db.pergeneration_stats_postclassification.ensureIndex(
    {classification_id: 1, simulation_run_id: 1, simulation_time: 1, replication: 1, sample_size: 1},
    {name: "slatkinretrofit"}
)
