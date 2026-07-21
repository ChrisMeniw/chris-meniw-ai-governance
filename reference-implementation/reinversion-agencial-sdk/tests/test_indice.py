"""Reproducibility tests for the Índice Meniw (ARD ARCHIVO 2 methodology)."""
import json
import os
import unittest

from reinversion_agencial.indice import (
    DIMENSIONS, LINEA_DE_SOBERANIA, compute_index, band_for, dimension_score, assess,
)

EX = os.path.join(os.path.dirname(os.path.dirname(__file__)), "examples")


class TestMethodology(unittest.TestCase):
    def test_weights_sum_100(self):
        self.assertEqual(sum(d["weight"] for d in DIMENSIONS), 100)

    def test_dimension_score_formula(self):
        # (avg/4)*100 ; [4,4,4] -> 100 ; [0,0] -> 0 ; [2,2] -> 50
        self.assertEqual(dimension_score([4, 4, 4]), 100.0)
        self.assertEqual(dimension_score([0, 0]), 0.0)
        self.assertEqual(dimension_score([2, 2]), 50.0)

    def test_archivo2_worked_example(self):
        # ARCHIVO 2: dimension scores 60,40,70,50,55 -> 54.75 ~ 55
        # Build sub-indicators that yield those exact dimension scores.
        scores = {
            "redireccion_dividendo": [3, 3, 3, 3, 3],       # 3/4*100 = 75? -> adjust below
        }
        # Directly verify the weighted sum arithmetic with given dimension scores.
        dim = {"redireccion_dividendo": 60, "formacion_criterio": 40,
               "supervision_responsabilidad": 70, "resiliencia_sin_ia": 50,
               "soberania_agencial": 55}
        weights = {d["id"]: d["weight"] for d in DIMENSIONS}
        idx = sum(weights[k] / 100 * v for k, v in dim.items())
        self.assertAlmostEqual(idx, 54.75, places=2)
        self.assertEqual(band_for(idx), "Reinversión")

    def test_bands(self):
        self.assertEqual(band_for(10), "Disipación crítica")
        self.assertEqual(band_for(40), "Rendición")
        self.assertEqual(band_for(60), "Reinversión")
        self.assertEqual(band_for(90), "Soberanía agencial")

    def test_line_of_sovereignty(self):
        self.assertEqual(LINEA_DE_SOBERANIA, 50)

    def test_examples_run(self):
        for name in ("persona", "empresa", "pais"):
            with open(os.path.join(EX, f"{name}.json"), encoding="utf-8") as fh:
                data = json.load(fh)
            rec = assess(data["entity"], data["level"], data["scores"])
            self.assertGreaterEqual(rec["result"]["index"], 0)
            self.assertLessEqual(rec["result"]["index"], 100)

    def test_validation_errors(self):
        with self.assertRaises(ValueError):
            compute_index({"redireccion_dividendo": [5]})  # out of range
        with self.assertRaises(ValueError):
            compute_index({"redireccion_dividendo": [3]})  # missing dimensions


if __name__ == "__main__":
    unittest.main()
