import unittest
import os
import logging
import shutil
import time

import matplotlib.pyplot as plt

from planobs import credentials
from planobs.plan import PlanObservation
from planobs.multiday_plan import MultiDayObservation
from planobs.api import Queue, APIError
from planobs import gcn_parser


class TestPlan(unittest.TestCase):
    def setUp(self):

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.max_distance_diff_arcsec = 2

    def test_gcn_parser(self):

        self.logger.info("\n\n Testing GCN parser \n\n")

        latest = gcn_parser.parse_latest_gcn_notice()

        self.logger.info(f"Length of latest GCN circular: {len(latest)}")

        self.assertGreater(len(latest), 0)

    def test_ztf_plan(self):

        self.logger.info("\n\n Testing ZTF Plan \n\n")

        name = "ZTF19accdntg"
        date = "2021-07-22"

        plan = PlanObservation(name=name, date=date, alertsource="ZTF")
        plan.plot_target()
        plan.request_ztf_fields()

        plt.close()

        recommended_field = plan.recommended_field
        recommended_field_expected = None

        self.assertEqual(recommended_field, recommended_field_expected)

    def test_icecube_plan(self):

        self.logger.info("\n\n Testing IceCube Plan \n\n")

        neutrino_name = "IC220624A"
        date = "2022-06-24"

        self.logger.info(f"Creating an observation plan for neutrino {neutrino_name}")
        plan = PlanObservation(name=neutrino_name, date=date, alertsource="icecube")
        plan.plot_target()
        plan.request_ztf_fields()

        plt.close()

        recommended_field = plan.recommended_field
        recommended_field_expected = 720

        self.logger.info(
            f"recommended field: {recommended_field}, expected {recommended_field_expected}"
        )
        self.assertEqual(recommended_field, recommended_field_expected)

    def test_icecube_multiday_plan(self):

        self.logger.info("\n\n Testing IceCube Multiday Plan \n\n")

        neutrino_name = "IC220501A"
        date = "2022-05-03"

        self.logger.info(
            f"Creating a multiday observation plan for neutrino {neutrino_name}"
        )
        plan = MultiDayObservation(
            name=neutrino_name, startdate=date, alertsource="icecube"
        )

        plt.close()

        plan.print_plan()
        plan.print_triggers()

        summary = plan.summarytext
        summary_expected = "\nYour multi-day observation plan for IC220501A\n-------------------------------------------------\ng-band observations\nNight 1 2022-05-03 10:35:00 - 2022-05-03 10:40:00\nNight 2 2022-05-04 10:38:00 - 2022-05-04 10:38:30\nNight 3 2022-05-05 10:37:00 - 2022-05-05 10:37:30\nNight 5 2022-05-07 10:35:00 - 2022-05-07 10:35:30\nNight 7 2022-05-09 10:33:00 - 2022-05-09 10:33:30\nNight 9 2022-05-11 10:30:00 - 2022-05-11 10:30:30\n-------------------------------------------------\n\n-------------------------------------------------\nr-band observations\nNight 1 2022-05-03 11:05:00 - 2022-05-03 11:10:00\nNight 9 2022-05-11 11:00:00 - 2022-05-11 11:00:30\n-------------------------------------------------\n\n"

        self.assertEqual(summary, summary_expected)

        triggers = plan.triggers

        q = Queue(user="DESY")

        for i, trigger in enumerate(triggers):
            q.add_trigger_to_queue(
                trigger_name=f"ToO_{neutrino_name}",
                validity_window_start_mjd=trigger["mjd_start"],
                field_id=trigger["field_id"],
                filter_id=trigger["filter_id"],
                exposure_time=trigger["exposure_time"],
            )

        q.print()

        triggers_summary = q.get_triggers()

        triggers_summary_expected = [
            (
                0,
                {
                    "user": "DESY",
                    "queue_name": "ToO_IC220501A_0",
                    "queue_type": "list",
                    "validity_window_mjd": [59702.44097222222, 59702.44444444444],
                    "targets": [
                        {
                            "request_id": 1,
                            "field_id": 593,
                            "filter_id": 1,
                            "subprogram_name": "ToO_Neutrino",
                            "program_pi": "Kulkarni",
                            "program_id": 2,
                            "exposure_time": 300,
                        }
                    ],
                },
            ),
            (
                1,
                {
                    "user": "DESY",
                    "queue_name": "ToO_IC220501A_1",
                    "queue_type": "list",
                    "validity_window_mjd": [59703.44305555556, 59703.44340277778],
                    "targets": [
                        {
                            "request_id": 1,
                            "field_id": 593,
                            "filter_id": 1,
                            "subprogram_name": "ToO_Neutrino",
                            "program_pi": "Kulkarni",
                            "program_id": 2,
                            "exposure_time": 30,
                        }
                    ],
                },
            ),
            (
                2,
                {
                    "user": "DESY",
                    "queue_name": "ToO_IC220501A_2",
                    "queue_type": "list",
                    "validity_window_mjd": [59704.44236111111, 59704.442708333336],
                    "targets": [
                        {
                            "request_id": 1,
                            "field_id": 593,
                            "filter_id": 1,
                            "subprogram_name": "ToO_Neutrino",
                            "program_pi": "Kulkarni",
                            "program_id": 2,
                            "exposure_time": 30,
                        }
                    ],
                },
            ),
            (
                3,
                {
                    "user": "DESY",
                    "queue_name": "ToO_IC220501A_3",
                    "queue_type": "list",
                    "validity_window_mjd": [59706.44097222222, 59706.44131944444],
                    "targets": [
                        {
                            "request_id": 1,
                            "field_id": 593,
                            "filter_id": 1,
                            "subprogram_name": "ToO_Neutrino",
                            "program_pi": "Kulkarni",
                            "program_id": 2,
                            "exposure_time": 30,
                        }
                    ],
                },
            ),
            (
                4,
                {
                    "user": "DESY",
                    "queue_name": "ToO_IC220501A_4",
                    "queue_type": "list",
                    "validity_window_mjd": [59708.43958333333, 59708.439930555556],
                    "targets": [
                        {
                            "request_id": 1,
                            "field_id": 593,
                            "filter_id": 1,
                            "subprogram_name": "ToO_Neutrino",
                            "program_pi": "Kulkarni",
                            "program_id": 2,
                            "exposure_time": 30,
                        }
                    ],
                },
            ),
            (
                5,
                {
                    "user": "DESY",
                    "queue_name": "ToO_IC220501A_5",
                    "queue_type": "list",
                    "validity_window_mjd": [59710.4375, 59710.43784722222],
                    "targets": [
                        {
                            "request_id": 1,
                            "field_id": 593,
                            "filter_id": 1,
                            "subprogram_name": "ToO_Neutrino",
                            "program_pi": "Kulkarni",
                            "program_id": 2,
                            "exposure_time": 30,
                        }
                    ],
                },
            ),
            (
                6,
                {
                    "user": "DESY",
                    "queue_name": "ToO_IC220501A_6",
                    "queue_type": "list",
                    "validity_window_mjd": [59702.461805555555, 59702.465277777774],
                    "targets": [
                        {
                            "request_id": 1,
                            "field_id": 593,
                            "filter_id": 2,
                            "subprogram_name": "ToO_Neutrino",
                            "program_pi": "Kulkarni",
                            "program_id": 2,
                            "exposure_time": 300,
                        }
                    ],
                },
            ),
            (
                7,
                {
                    "user": "DESY",
                    "queue_name": "ToO_IC220501A_7",
                    "queue_type": "list",
                    "validity_window_mjd": [59710.458333333336, 59710.45868055556],
                    "targets": [
                        {
                            "request_id": 1,
                            "field_id": 593,
                            "filter_id": 2,
                            "subprogram_name": "ToO_Neutrino",
                            "program_pi": "Kulkarni",
                            "program_id": 2,
                            "exposure_time": 30,
                        }
                    ],
                },
            ),
        ]

        self.assertEqual(triggers_summary, triggers_summary_expected)

        try:
            q.delete_queue()
        except APIError:
            self.logger.info("Queue was probably already empty")

        # Now we submit our triggers
        q.submit_queue()

        time.sleep(5)

        current_too_queue = q.get_too_queues()

        self.logger.info(
            f"Current Kowalski queue has {len(current_too_queue['data'])} entries (after submitting)"
        )

        kowalski_list = [
            current_too_queue["data"][i]["queue_name"]
            for i in range(len(current_too_queue["data"]))
        ]
        expected_list = [f"ToO_IC220501A_{i}" for i in range(8)]

        # All triggers should be submitted
        for t in expected_list:
            self.assertIn(t, kowalski_list)

        # Now we delete our triggers
        q.delete_queue()

        current_too_queue = q.get_too_queues()

        self.logger.info(
            f"Current Kowalski queue has {len(current_too_queue['data'])} entries (after deleting)"
        )

        kowalski_list = [
            current_too_queue["data"][i]["queue_name"]
            for i in range(len(current_too_queue["data"]))
        ]

        # All triggers should be deleted
        for t in expected_list:
            self.assertNotIn(t, kowalski_list)

    def tearDown(self):
        names = [
            "ZTF19accdntg",
            "IC220624A",
            "IC220501A",
        ]
        cwd = os.getcwd()

        for name in names:
            if os.path.exists(os.path.join(cwd, name)):
                shutil.rmtree(name)
