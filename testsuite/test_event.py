# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4
#
# gst-python - Python bindings for GStreamer
# Copyright (C) 2002 David I. Lehn
# Copyright (C) 2004 Johan Dahlin
# Copyright (C) 2005 Edward Hervey
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA

import os
import sys
from common import gst, unittest, testhelper, TestCase

class EventTest(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.pipeline = gst.parse_launch('fakesrc ! fakesink name=sink')
        self.sink = self.pipeline.get_by_name('sink')
        self.pipeline.set_state(gst.STATE_PLAYING)

    def tearDown(self):
        gst.debug('setting pipeline to NULL')
        self.pipeline.set_state(gst.STATE_NULL)
        gst.debug('set pipeline to NULL')

        del self.sink
        del self.pipeline
        TestCase.tearDown(self)
        
    def testEventSeek(self):
        # this event only serves to change the rate of data transfer
        event = gst.event_new_seek(1.0, gst.FORMAT_BYTES, gst.SEEK_FLAG_FLUSH,
            gst.SEEK_TYPE_NONE, 0, gst.SEEK_TYPE_NONE, 0)
        # FIXME: but basesrc goes into an mmap/munmap spree, needs to be fixed

        event = gst.event_new_seek(1.0, gst.FORMAT_BYTES, gst.SEEK_FLAG_FLUSH,
            gst.SEEK_TYPE_SET, 0, gst.SEEK_TYPE_NONE, 0)
        assert event
        gst.debug('sending event')
        self.sink.send_event(event)
        gst.debug('sent event')

    def testWrongEvent(self):
        buffer = gst.Buffer()
        self.assertRaises(TypeError, self.sink.send_event, buffer)
        number = 1
        self.assertRaises(TypeError, self.sink.send_event, number)


# FIXME: fix these tests
#class EventFileSrcTest(unittest.TestCase):
#    # FIXME: properly create temp files
#    filename = '/tmp/gst-python-test-file'
#    def setUp(self):
#        if os.path.exists(self.filename):
#            os.remove(self.filename)
#        open(self.filename, 'w').write(''.join(map(str, range(10))))
#                
#        self.pipeline = gst.parse_launch('filesrc name=source location=%s blocksize=1 ! fakesink signal-handoffs=1 name=sink' % self.filename)
#        self.source = self.pipeline.get_by_name('source')
#        self.sink = self.pipeline.get_by_name('sink')
#        self.sink.connect('handoff', self.handoff_cb)
#        self.bus = self.pipeline.get_bus()
#        self.pipeline.set_state(gst.STATE_PLAYING)
#        
#    def tearDown(self):
#        assert self.pipeline.set_state(gst.STATE_PLAYING)
#        if os.path.exists(self.filename):
#            os.remove(self.filename)
#
#    def handoff_cb(self, element, buffer, pad):
#        self.handoffs.append(str(buffer))
#
#    def playAndIter(self):
#        self.handoffs = []
#        assert self.pipeline.set_state(gst.STATE_PLAYING)
#        while 42:
#            msg = self.bus.pop()
#            if msg and msg.type == gst.MESSAGE_EOS:
#                break
#        assert self.pipeline.set_state(gst.STATE_PAUSED)
#        handoffs = self.handoffs
#        self.handoffs = []
#        return handoffs
#
#    def sink_seek(self, offset, method=gst.SEEK_METHOD_SET):
#        method |= (gst.SEEK_FLAG_FLUSH | gst.FORMAT_BYTES)
#        self.source.send_event(gst.event_new_seek(method, offset))
#        self.source.send_event(gst.Event(gst.EVENT_FLUSH)) 
#        self.sink.send_event(gst.event_new_seek(method, offset))
#        self.sink.send_event(gst.Event(gst.EVENT_FLUSH))
#       
#    def testSimple(self):
#        handoffs = self.playAndIter()
#        assert handoffs == map(str, range(10))
#    
#    def testSeekCur(self):
#        self.sink_seek(8)
#        
#        #print self.playAndIter()

class TestEmit(TestCase):
    def testEmit(self):
        object = testhelper.get_object()
        object.connect('event', self._event_cb)
        
        # First emit from C
        testhelper.emit_event(object)

        # Then emit from Python
        object.emit('event', gst.event_new_eos())
        
    def _event_cb(self, obj, event):
        assert isinstance(event, gst.Event)
    

if __name__ == "__main__":
    unittest.main()
