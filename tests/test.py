import unittest
from bedshift import bedshift
from bedshift.bedshift import handle_yaml

class TestBedshift(unittest.TestCase):
    def setUp(self):
        self.bs = bedshift.Bedshift('tests/test.bed', chrom_sizes="tests/hg38.chrom.sizes")

    def test_add(self):
        added = self.bs.add(0.1, 100, 20)
        self.assertEqual(added, 1000)
        self.bs.reset_bed()

    def test_add_high_rate(self):
        added = self.bs.add(1.23, 500, 123)
        self.assertEqual(added, 12300)
        self.bs.reset_bed()

    def test_add_from_file(self):
        added = self.bs.add_from_file("tests/test.bed", 0.25)
        self.assertEqual(added, 2500)
        self.bs.reset_bed()

    def test_drop(self):
        dropped = self.bs.drop(0.315)
        self.assertEqual(dropped, 3150)
        self.bs.reset_bed()

    def test_shift(self):
        shifted = self.bs.shift(0.129, 200, 30)
        self.assertEqual(shifted, 1290)
        self.bs.reset_bed()

    def test_cut(self):
        cut = self.bs.cut(0.909)
        self.assertEqual(cut, 9090)
        self.bs.reset_bed()

    def test_merge(self):
        merged = self.bs.merge(0.2)
        self.assertEqual(merged, 2000)
        self.bs.reset_bed()

    def test_combo(self):
        _ = self.bs.drop(0.4)
        _ = self.bs.add(0.2, 200, 10)
        self.assertEqual(len(self.bs.bed), 7200)
        self.bs.reset_bed()
		
    def test_drop_from_file_high_rate(self):
        dropped = self.bs.drop_from_file("tests/test.bed", 1)
        self.assertEqual(dropped, 10000)
        self.bs.reset_bed()

    def test_drop_from_file_zero_rate(self):
        dropped = self.bs.drop_from_file("tests/test.bed", 0)
        self.assertEqual(dropped, 0)
        self.bs.reset_bed()

    def test_handle_yaml(self):
        yamled = handle_yaml(bedshifter=self.bs, yaml_fp="tests/bedshift_analysis.yaml")
        self.bs.reset_bed()

        added = self.bs.add(addrate=0.1, addmean=100, addstdev=20)
        f_added_10 = self.bs.add_from_file(fp="tests/test.bed", addrate=0.1)
        f_dropped_15 = self.bs.drop_from_file(fp="tests/test.bed", droprate=0.1)
        f_added_20 = self.bs.add_from_file(fp="tests/test.bed", addrate=0.2)
        cut = self.bs.cut(cutrate=0.20)
        shifted = self.bs.shift(shiftrate=0.30, shiftmean=100, shiftstdev=200)
        merged = self.bs.merge(mergerate=0.15)
        # dropped = self.bs.drop(droprate=0.30)
        # print("dropped", dropped)

        total = added+f_added_10+f_dropped_15+f_added_20+cut+shifted+merged#+dropped

        self.assertEqual(yamled, total)
        self.bs.reset_bed()

	def test_all_perturbations1(self):
		perturbed = self.bs.all_perturbations(
							addrate=0.5, addmean=320.0, addstdev=20.0,
							shiftrate=0.23, shiftmean=-10.0, shiftstdev=120.0,
							cutrate=0.12,
							droprate=0.42)
		self.assertEqual(perturbed, 16156)
		self.assertEqual(len(self.bs.bed), 9744)
		self.bs.reset_bed()

	def test_all_perturbations2(self):
		perturbed = self.bs.all_perturbations(
							addrate=0.3, addmean=320.0, addstdev=20.0,
							shiftrate=0.3, shiftmean=-10.0, shiftstdev=120.0,
							cutrate=0.1,
							mergerate=0.11,
							droprate=0.03)
		# merge sometimes merges more or less than expected because it depends
		# if the randomly chosen regions are adjacent
		self.assertAlmostEqual(perturbed, 9250, places=-2)

	def test_to_bed(self):
		self.bs.to_bed('py_output.bed')
