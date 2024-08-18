package org.example;

import java.io.IOException;
import java.io.InputStream;
import java.util.Objects;

import com.fasterxml.jackson.core.exc.StreamReadException;
import com.fasterxml.jackson.databind.DatabindException;
import com.fasterxml.jackson.databind.ObjectMapper;

public class Main {
    static ObjectMapper mapper = new ObjectMapper();
    public static void main(String[] args) throws StreamReadException, DatabindException, IOException {
        // Get params from input.json
        InputStream initParams = Main.class.getClassLoader().getResourceAsStream("input.json");

        // Parse the params
        SimulationParams params = mapper.readValue(initParams,SimulationParams.class);

        if(Objects.equals(params.dimension(), "2D")){
            var simulation = new GOLSimulation<>(new Grid2D(params.m(), params.initializationRadius(), params.initializationPercentage(), params.RandomInitialConditions()) );
            simulation.start("simulationOutput.json");

        } else if (Objects.equals(params.dimension(), "3D")){
            var simulation = new GOLSimulation<>(new Grid3D(params.m(), params.initializationRadius(), params.initializationPercentage(), params.RandomInitialConditions()) );
            simulation.start("simulationOutput3D.json");
        } else {
            throw new RuntimeException("Invalid param for dimension");
        }


    }
}