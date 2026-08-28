import copy
import unittest

import npp_e
import transform_npp_e


class TransformNppETest(unittest.TestCase):
    def setUp(self) -> None:
        self.baseline = npp_e.build_snapshot(npp_e.sample_artifacts())

    def test_sufficient_design_evolves_named_baseline(self) -> None:
        result = transform_npp_e.transform(self.baseline, transform_npp_e.sufficient_design())
        self.assertEqual(self.baseline["id"], transform_npp_e.BASELINE_SNAPSHOT_ID)
        self.assertNotEqual(result["id"], self.baseline["id"])
        npp_e.verify_snapshot(result)
        self.assertEqual(len(result["artifacts"]), 5)

    def test_insufficient_design_refuses_before_writing(self) -> None:
        with self.assertRaises(npp_e.Refusal) as caught:
            transform_npp_e.transform(self.baseline, transform_npp_e.insufficient_design())
        self.assertEqual(caught.exception.evidence["reason"], "insufficient_design")
        self.assertEqual(caught.exception.evidence["rules"], ["TR-L4"])
        self.assertTrue(caught.exception.evidence["nothing_proceeded"])

    def test_grounding_requires_exact_baseline_identity(self) -> None:
        design = transform_npp_e.sufficient_design()
        design["grounding"]["entries"][0]["baseline_snapshot_id"] = "snapshot:remembered"
        with self.assertRaises(npp_e.Refusal) as caught:
            transform_npp_e.transform(self.baseline, design)
        self.assertEqual(caught.exception.evidence["reason"], "insufficient_design")
        self.assertEqual(caught.exception.evidence["rules"], ["TR-L2"])

    def test_wrong_supplied_baseline_is_refused(self) -> None:
        wrong_baseline = copy.deepcopy(self.baseline)
        wrong_baseline["id"] = "snapshot:wrong"
        with self.assertRaises(npp_e.Refusal) as caught:
            transform_npp_e.transform(wrong_baseline, transform_npp_e.sufficient_design())
        self.assertEqual(caught.exception.evidence["reason"], "baseline_identity_mismatch")
        self.assertEqual(caught.exception.evidence["rules"], ["TR-15"])
        self.assertTrue(caught.exception.evidence["nothing_proceeded"])

    def test_runtime_records_loan_and_refuses_second_loan(self) -> None:
        runtime = transform_npp_e.LibraryRuntime(transform_npp_e.transform(self.baseline, transform_npp_e.sufficient_design()))
        runtime.lend("copy-1", "member-1")
        self.assertEqual(runtime.loan_status("copy-1"), {"copy_id": "copy-1", "on_loan": True, "loan": {"copy_id": "copy-1", "member_id": "member-1"}})
        with self.assertRaises(npp_e.Refusal) as caught:
            runtime.lend("copy-1", "member-2")
        self.assertEqual(caught.exception.evidence["reason"], "copy_already_on_loan")

    def test_execution_routes_declared_failure_outcome(self) -> None:
        runtime = transform_npp_e.LibraryRuntime(transform_npp_e.transform(self.baseline, transform_npp_e.sufficient_design()))
        runtime.execute("copy-1", "member-1")
        result = runtime.execute("copy-1", "member-2")
        self.assertEqual(result["outcome"], "failed")
        self.assertEqual(result["terminal"], "loan-rejected")

    def test_undeclared_capability_outcome_refuses(self) -> None:
        runtime = transform_npp_e.LibraryRuntime(transform_npp_e.transform(self.baseline, transform_npp_e.sufficient_design()))
        runtime._dispatch = lambda capability, copy_id, member_id: ("unexpected", None)
        with self.assertRaises(npp_e.Refusal) as caught:
            runtime.execute("copy-1", "member-1")
        self.assertEqual(caught.exception.evidence["reason"], "undeclared_outcome")

    def test_runtime_status_for_unloaned_copy_is_established(self) -> None:
        runtime = transform_npp_e.LibraryRuntime(transform_npp_e.transform(self.baseline, transform_npp_e.sufficient_design()))
        self.assertEqual(runtime.loan_status("copy-2"), {"copy_id": "copy-2", "on_loan": False, "loan": None})

    def test_execution_reports_declared_outcome_and_reads_declared_route(self) -> None:
        runtime = transform_npp_e.LibraryRuntime(transform_npp_e.transform(self.baseline, transform_npp_e.sufficient_design()))
        result = runtime.execute("copy-1", "member-1")
        self.assertEqual(result["outcome"], "completed")
        self.assertEqual(result["path"], ["lend-copy-to-member"])
        self.assertEqual(result["terminal"], "loan-recorded")

    def test_unrouted_declared_outcome_refuses(self) -> None:
        snapshot = transform_npp_e.transform(self.baseline, transform_npp_e.sufficient_design())
        workflow = next(item for item in snapshot["artifacts"] if item["kind"] == "workflow")
        workflow["declaration"]["steps"][0]["routes"].pop("completed")
        workflow["id"] = npp_e.artifact_id(workflow["kind"], workflow["version"], workflow["governance"], workflow["declaration"])
        snapshot = npp_e.build_snapshot(snapshot["artifacts"])
        with self.assertRaises(npp_e.Refusal) as caught:
            transform_npp_e.LibraryRuntime(snapshot).execute("copy-1", "member-1")
        self.assertEqual(caught.exception.evidence["reason"], "unrouted_outcome")

    def test_routing_mutation_changes_execution_path(self) -> None:
        snapshot = transform_npp_e.transform(self.baseline, transform_npp_e.sufficient_design())
        workflow = next(item for item in snapshot["artifacts"] if item["kind"] == "workflow")
        workflow["declaration"]["steps"][0]["routes"]["completed"] = "alternate-terminal"
        workflow["id"] = npp_e.artifact_id(workflow["kind"], workflow["version"], workflow["governance"], workflow["declaration"])
        snapshot["constituents"] = [{"id": item["id"], "integrity": npp_e.digest(item)} for item in sorted(snapshot["artifacts"], key=lambda item: item["id"])]
        content = {key: snapshot[key] for key in snapshot["whole_integrity_covers"]}
        snapshot["whole_integrity"] = npp_e.digest(content)
        snapshot["id"] = "snapshot:" + npp_e.digest(content)
        with self.assertRaises(npp_e.Refusal) as caught:
            transform_npp_e.LibraryRuntime(snapshot).execute("copy-1", "member-1")
        self.assertEqual(caught.exception.evidence["reason"], "unresolved_route_target")

    def test_missing_workflow_refuses_execution(self) -> None:
        snapshot = transform_npp_e.transform(self.baseline, transform_npp_e.sufficient_design())
        artifacts = [item for item in snapshot["artifacts"] if item["kind"] != "workflow"]
        with self.assertRaises(npp_e.Refusal) as caught:
            transform_npp_e.LibraryRuntime(npp_e.build_snapshot(artifacts))
        self.assertEqual(caught.exception.evidence["reason"], "missing_workflow")

    def test_same_declared_answers_produce_same_result(self) -> None:
        first = transform_npp_e.transform(self.baseline, transform_npp_e.sufficient_design())
        second = transform_npp_e.transform(copy.deepcopy(self.baseline), copy.deepcopy(transform_npp_e.sufficient_design()))
        self.assertEqual(first, second)

    def test_every_declared_rule_can_refuse(self) -> None:
        mutations = {
            "TR-L1": lambda design: design["need"]["entries"][0].update(statement=""),
            "TR-L2": lambda design: design["grounding"]["entries"][0].update(baseline_snapshot_id="snapshot:wrong"),
            "TR-L3": lambda design: design["grounding"]["entries"][0].update(artifacts=["artifact:missing"]),
            "TR-L4": lambda design: design["design"]["entries"][0].update(inputs=["member_id"]),
            "TR-L5": lambda design: design["design"]["entries"][0].update(inputs=["copy_id"]),
            "TR-L6": lambda design: design["schedule"]["entries"][0].update(target=""),
        }
        for rule_id, mutate in mutations.items():
            design = transform_npp_e.sufficient_design()
            mutate(design)
            with self.subTest(rule_id=rule_id), self.assertRaises(npp_e.Refusal) as caught:
                transform_npp_e.transform(self.baseline, design)
            self.assertIn(rule_id, caught.exception.evidence["rules"])

    def test_unknown_check_kind_refuses_hard(self) -> None:
        design = transform_npp_e.sufficient_design()
        design["rules"][0]["check"] = "invented_check"
        with self.assertRaises(npp_e.Refusal) as caught:
            transform_npp_e.transform(self.baseline, design)
        self.assertEqual(caught.exception.evidence["reason"], "unknown_check_kind")


if __name__ == "__main__":
    unittest.main()