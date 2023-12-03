# def gen_prim(self):
#     return Primitive('primitive', [], 50, 100, 100, 50)
#
#
# def gen_block(self, depth, prob_inner, prob_block, n_inner=2):
#     max_depth = 3
#
#     primitive = Primitive('primitive', [], 50, 100, 100, 50)
#     block_top = Block('block', [], [], 100, 100, block_width, block_height)
#
#     if depth < max_depth and random.random() < prob_inner:
#         block_top.set_inner_block_list(
#             [self.gen_block(depth + 1, prob_inner=prob_inner, prob_block=prob_block) if random.random() < prob_block
#              else primitive for i in range(1, n_inner)])
#     print(depth)
#     return block_top
#
#
# def gen_objects(self, n_prim=5, n_block=10, prob_inner=0.8, prob_block=0.5):
#     for i in range(1, random.randrange(2, n_prim)):
#         self.work_zone.rendering_widget.add_primitive(self.gen_prim())
#
#     for i in range(1, random.randrange(2, n_block)):
#         self.work_zone.rendering_widget.add_block(self.gen_block(depth=0, prob_inner=prob_inner, prob_block=prob_block))