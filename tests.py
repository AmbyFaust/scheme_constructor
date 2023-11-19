import sys
from PyQt5.QtWidgets import QApplication

import unittest

from gui.object_item import ObjectItem, _ObjectDublicator, Primitive, PrimitiveWidget, Block, BlockWidget
from gui.object_panel import ObjectPanel

class ObjectPanelModuleTest(unittest.TestCase):

### ObjectItem
####### testing cloning 
    def test_primitive_cloning(self):
        primitive = Primitive("", [], (0,0), 1, 1)
        primitive_widget = PrimitiveWidget(None, primitive=primitive)
        cloned = _ObjectDublicator.clone(primitive_widget)
        self.assertIsNotNone(cloned)
        self.assertIsNot(cloned, primitive_widget)


    def test_block_cloning(self):
        block = Block("", [], [], [], (0,0), 1, 1)
        block_widget = BlockWidget(None, block=block)
        cloned = _ObjectDublicator.clone(block_widget)
        self.assertIsNotNone(cloned)
        self.assertIsNot(cloned, block_widget)


    def test_other_cloning(self):
        block = Block("", [], [], [], (0,0), 1, 1)
        self.assertIsNone(_ObjectDublicator.clone(block))
#######

### ObjectPanel
####### testing registration
    def test_primitive_registration(self):
        object_panel = ObjectPanel()
        count = object_panel.count()

        primitive = Primitive("test", [], (0,0), 1, 1)
        primitive_widget = PrimitiveWidget(None, primitive=primitive)
        object_panel.registerObject(primitive_widget)

        self.assertGreater(object_panel.count(), count)
        stored_primitive = object_panel.item(2).getStoredObject()
        self.assertEqual(stored_primitive.name_label.text(), "test")


    def test_block_registration(self):
        object_panel = ObjectPanel()
        count = object_panel.count()

        block = Block("test", [], [], [], (0,0), 1, 1)
        block_widget = BlockWidget(None, block=block)
        object_panel.registerObject(block_widget)

        self.assertGreater(object_panel.count(), count)
        stored_block = object_panel.item(3).getStoredObject()
        self.assertEqual(stored_block.name_label.text(), "test")


    def test_editing_object(self): # aka register primitve/block with same name 
        object_panel = ObjectPanel()
        block = Block("test", [], [], [], (0,0), 1, 1)
        block_widget = BlockWidget(None, block=block)
        object_panel.registerObject(block_widget)
        count = object_panel.count()

        new_block = Block("test", [], [], [], (10,10), 1, 1)
        block_widget = BlockWidget(None, block=new_block)
        object_panel.registerObject(block_widget)

        self.assertEqual(object_panel.count(), count)
        stored_block = object_panel.item(3).getStoredObject()
        self.assertEqual(stored_block.block.get_top_left(), (10, 10))

#######


if __name__ == '__main__':
    app = QApplication(sys.argv)
    unittest.main()