# Copyright (c) $today.year.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Creative Commons-GNU General Public Llicense 2.0, as "non-commercial/sharealike".  You may use, modify, and distribute this software for non-commercial purposes, and you must distribute any modifications under the same license.  
#
# For detailed license terms, see:
# http://creativecommons.org/licenses/GPL/2.0/



import unittest
import ctpy.data as data
import pprint as pp
import ming
from bson.objectid import ObjectId


class TestUpdateData(unittest.TestCase):

    def setUp(self):
        data.set_database_port("27017")
        data.set_database_hostname("localhost")
        data.set_experiment_name("testupdate")
        config = data.getMingConfiguration()
        ming.configure(**config)

        # clean out the collection
        data.PerGenerationStatsPostclassification.m.remove()

        self.data = dict(
            simulation_time=1000,
            classification_id=ObjectId("52056c3b3f07d50754eec1a3"),
            classification_type="EVEN",
            classification_dim=2,
            classification_coarseness=4,
            replication=0,
            sample_size=50,
            population_size=2000,
            mutation_rate=0.01,
            simulation_run_id="urn:uuid:07f75571-6f6b-4113-84c5-46cb8114cb72",
            mode_richness=[5,3],
            class_richness=2,
            mode_evenness_iqv=[0.5,0.3],
            class_evenness_iqv=0.25,
            design_space_occupation=None,
            class_innovation_interval_times=None
        )

    def test_update(self):
        updateValue = 5000
        data.PerGenerationStatsPostclassification(self.data).m.save()

        record = data.PerGenerationStatsPostclassification.m.find().first()
        data.updateFieldSimrunStatsPostclassification(record._id, "sample_size", updateValue)


        #record["sample_size"] = 5000
        #record.m.save()

        record2 = data.PerGenerationStatsPostclassification.m.find().first()
        self.assertEqual(updateValue, record2.sample_size)


if __name__ == "__main__":
    unittest.main()

