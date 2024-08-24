package org.example;

import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.IntStream;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.example.records.AllSimulationParams;
import org.example.records.SingleSimulationParams;

public class Main {
    static ObjectMapper mapper = new ObjectMapper();
    public static void main(String[] args) throws IOException {
        // Get params from input.json
        InputStream initParams = Main.class.getClassLoader().getResourceAsStream("input.json");

        // Parse all the desired run configurations
        AllSimulationParams allSimulationParams = mapper.readValue(initParams, AllSimulationParams.class);

        // Generate list of run configurations
        List<SingleSimulationParams> singleSimulationParamsList = generateSingleSimulationParamsList(allSimulationParams);

        // Get the current timestamp
        String timeStamp = new SimpleDateFormat("yyyyMMdd_HHmmss").format(new Date());

        // Generate output json file name that has current timestamp
        String filenameWithTimestamp = "simulation_" + timeStamp + ".json";

        // Invoke every simulation from the generated list
        final AtomicInteger simulationCounter = new AtomicInteger(0);
        try (FileWriter writer = initializeOutputJson(allSimulationParams, filenameWithTimestamp)){
            singleSimulationParamsList.forEach(params -> {
                try {
                    callSimulation(params, writer, simulationCounter.incrementAndGet(), singleSimulationParamsList.size());
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            });
            writer.write("\n]\n}");
        }
    }

    private static FileWriter initializeOutputJson(AllSimulationParams global_params, String outputJsonName) throws IOException {
        FileWriter writer = new FileWriter("./files/%s".formatted(outputJsonName));
        writer.write("{\n\"global_params\": ");
        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        gson.toJson(global_params, writer);
        writer.write(",\n");
        writer.write("\"simulations\": [\n");
        return writer;
    }

    private static void callSimulation(SingleSimulationParams params, FileWriter writer, int simulationNumber, int totalSimulations) throws IOException {
        System.out.printf("Starting simulation %d of %d\n", simulationNumber, totalSimulations);
        if (simulationNumber > 1){
            writer.write(',');
        }
        if(Objects.equals(params.dimension(), "2D")){
            var simulation = new GOLSimulation<>(new Grid2D(params.m(), params.initializationRadius(), params.initializationPercentage(), params.randomInitialConditions()), params );
            simulation.start(writer);
        } else if (Objects.equals(params.dimension(), "3D")){
            var simulation = new GOLSimulation<>(new Grid3D(params.m(), params.initializationRadius(), params.initializationPercentage(), params.randomInitialConditions()), params );
            simulation.start(writer);
        } else {
            throw new RuntimeException("Invalid param for dimension");
        }
    }

    private static List<SingleSimulationParams> generateSingleSimulationParamsList(AllSimulationParams allSimulationParams) {
        List<SingleSimulationParams> singleSimulationParamsList = new ArrayList<>();
        List<Double> initializationPercentages = allSimulationParams.initializationPercentages();
        allSimulationParams.rulesets().forEach((dimension, rulesetMap) -> {
            rulesetMap.forEach((rulesetName, ruleset) -> {
                initializationPercentages.forEach(initializationPercentage -> {
                    IntStream.range(0, allSimulationParams.repetitions()).forEach(repetition_id -> {
                        singleSimulationParamsList.add(new SingleSimulationParams(
                                (Objects.equals(dimension, "2D") ? allSimulationParams.m2D() : allSimulationParams.m3D()),
                                (Objects.equals(dimension, "2D") ? allSimulationParams.initializationRadius2D() : allSimulationParams.initializationRadius3D()),
                            initializationPercentage,
                            allSimulationParams.randomInitialConditions(),
                            allSimulationParams.maxEpochs(),
                            dimension,
                            ruleset,
                            repetition_id
                        ));
                    });
                });
            });
        });
        return singleSimulationParamsList;
    }
}