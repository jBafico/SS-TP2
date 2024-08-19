package org.example.records;

import java.util.Map;
import java.util.List;

public record AllSimulationParams(
    int m2D,
    int initializationRadius2D,
    int m3D,
    int initializationRadius3D,
    List<Double> initializationPercentages,
    boolean randomInitialConditions,
    int maxEpochs,
    int repetitions,
    Map<String, Map<String, Ruleset>> rulesets
) {
}



