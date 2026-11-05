import importlib.util
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('model',ROOT/'churn_prediction_model.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ExperimentContract(unittest.TestCase):
 def test_held_out_scores_and_metrics(self):
  with tempfile.TemporaryDirectory() as d:
   metrics,train,test,scores=m.run(Path(d))
   self.assertFalse(set(train.id_cliente)&set(test.id_cliente))
   self.assertEqual(set(scores.id_cliente),set(test.id_cliente))
   self.assertTrue(scores.churn_risk_score.between(0,1).all())
   self.assertEqual(sum(map(sum,metrics['model']['confusion_matrix'])),len(test))
   self.assertEqual(metrics['baseline']['roc_auc'],.5)
 def test_seed_reproduces_input(self):self.assertTrue(m.simulate(seed=42).equals(m.simulate(seed=42)))
 def test_tiny_sample_rejected(self):
  with self.assertRaises(ValueError):m.simulate(10)
if __name__=='__main__':unittest.main()
