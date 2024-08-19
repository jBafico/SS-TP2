package org.example.records;

public record SingleSimulationParams (
    int m,
    int initializationRadius,
    double initializationPercentage,
    boolean randomInitialConditions,
    int maxEpochs,
    String dimension,
    Ruleset ruleset,
    int repetition_id
){}
