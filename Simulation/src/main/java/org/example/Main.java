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


        InputStream initParams = Main.class.getClassLoader().getResourceAsStream("input.json");


        SimulationParams params = mapper.readValue(initParams,SimulationParams.class);

        if(Objects.equals(params.dimension(), "2D")){
            var simulation = new GOLSimulation<Cell[][]>(new Grid2D(params.m(), params.initializationRadius(), params.initializationPercentage(), params.RandomInitialConditions()) );

            //Arranco la Simulacion
            simulation.start();


        }else{
            //TODO 3D Simulation
        }


    }
}