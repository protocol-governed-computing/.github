import copy
import unittest

import npp_e


class NppETest(unittest.TestCase):
    def setUp(self) -> None:
        self.artifacts = npp_e.sample_artifacts()
        self.snapshot = npp_e.build_snapshot(self.artifacts)

    def test_valid_snapshot_is_rederivable(self) -> None:
        npp_e.verify_snapshot(self.snapshot)
        inspection = npp_e.Inspection(self.snapshot)
        self.assertEqual(inspection.snapshot_identity(), self.snapshot["id"])
        self.assertEqual(len(inspection.enumerate_artifacts()), 2)
        self.assertEqual(inspection.get_artifact(self.artifacts[0]["id"]), self.artifacts[0])

    def test_unknown_kind_is_rule_refusal(self) -> None:
        unknown = npp_e.make_artifact("constitution", self.artifacts[0]["declaration"], governance=None)
        unknown["kind"] = "unregistered-kind"
        with self.assertRaises(npp_e.Refusal) as caught:
            npp_e.admit([unknown], genesis=True)
        self.assertEqual(caught.exception.evidence["cause"], "rule_refusal")
        self.assertEqual(caught.exception.evidence["consequence"], "refuse")
        self.assertTrue(caught.exception.evidence["nothing_proceeded"])
        self.assertIn("KV-2", caught.exception.evidence["rules"])

    def test_duplicate_identity_is_rule_refusal(self) -> None:
        with self.assertRaises(npp_e.Refusal) as caught:
            npp_e.admit([self.artifacts[0], self.artifacts[0]], genesis=True)
        self.assertEqual(caught.exception.evidence["cause"], "rule_refusal")
        self.assertEqual(caught.exception.evidence["rules"], ["MB-6", "ID-4"])

    def test_corrupted_snapshot_is_refused_before_inspection(self) -> None:
        corrupted = copy.deepcopy(self.snapshot)
        corrupted["artifacts"][1]["declaration"]["answer"] = "altered"
        with self.assertRaises(npp_e.Refusal) as caught:
            npp_e.Inspection(corrupted)
        self.assertEqual(caught.exception.evidence["reason"], "whole_integrity_mismatch")
        self.assertTrue(caught.exception.evidence["nothing_proceeded"])

    def test_absent_named_artifact_is_refusal_not_empty(self) -> None:
        with self.assertRaises(npp_e.Refusal) as caught:
            npp_e.Inspection(self.snapshot).get_artifact("artifact:absent")
        self.assertEqual(caught.exception.evidence["reason"], "absent_named_artifact")
        self.assertEqual(caught.exception.evidence["cause"], "rule_refusal")

    def test_deterministic_reconstruction(self) -> None:
        rebuilt = npp_e.build_snapshot(copy.deepcopy(self.artifacts))
        self.assertEqual(rebuilt, self.snapshot)

    def test_integrity_algorithm_is_sha256(self) -> None:
        semantic_content = {"z": [1, True], "a": "NPP-E"}
        self.assertEqual(
            npp_e.digest(semantic_content),
            "a0eb844e8eaab8658d5f227a6dd20a3b993d96b63ab0bdd89dda3acf98094fa9",
        )


if __name__ == "__main__":
    unittest.main()
