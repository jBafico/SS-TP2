package org.example;

import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;

import com.fasterxml.jackson.core.exc.StreamReadException;
import com.fasterxml.jackson.databind.DatabindException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class Main {
    static ObjectMapper mapper = new ObjectMapper();
    public static void main(String[] args) throws IOException {
        // Get params from input.json
        InputStream initParams = Main.class.getClassLoader().getResourceAsStream("input.json");

        // Parse the params as an array of SimulationParams
        SimulationParams[] paramsArray = mapper.readValue(initParams, SimulationParams[].class);

        // If you need to work with a List instead of an array
        List<SimulationParams> paramsList = Arrays.asList(paramsArray);

        paramsList.forEach(params -> {
            try {
                callSimulation(params);
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        });
    }

    private static void callSimulation(SimulationParams params) throws IOException {
        if(Objects.equals(params.dimension(), "2D")){
            var simulation = new GOLSimulation<>(new Grid2D(params.m(), params.initializationRadius(), params.initializationPercentage(), params.RandomInitialConditions()), params );
            simulation.start("simulationOutput.json");

        } else if (Objects.equals(params.dimension(), "3D")){
            var simulation = new GOLSimulation<>(new Grid3D(params.m(), params.initializationRadius(), params.initializationPercentage(), params.RandomInitialConditions()), params );
            simulation.start("simulationOutput3D.json");
        } else {
            throw new RuntimeException("Invalid param for dimension");
        }
    }
}