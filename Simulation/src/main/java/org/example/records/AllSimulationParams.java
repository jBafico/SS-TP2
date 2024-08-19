package org.example.records;

import java.util.Map;
import java.util.List;

public record AllSimulationParams(
    int m,
    int initializationRadius,
    List<Double> initializationPercentages,
    boolean randomInitialConditions,
    int maxEpochs,
    int repetitions,
    Map<String, Map<String, Ruleset>> rulesets
) {
}



