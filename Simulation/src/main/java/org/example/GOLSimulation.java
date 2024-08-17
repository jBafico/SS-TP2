package org.example;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

//For keeping history

@Getter
@RequiredArgsConstructor
public class GOLSimulation<TMatrix> {
    private final GridAbstract<TMatrix> currentGrid;

    public void start() throws IOException {
        //TODO VER COMO ESCRIBIR EL JSON DINAMICAMENTE CON EL FORMATO CORRECTO
        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        try (FileWriter writer = new FileWriter("../files/simulationOutput.json")) {
            System.out.println("Simulation started");
            gson.toJson(currentGrid.matrix, writer);
            while (!currentGrid.isFinished()) {
                currentGrid.evolve();
                gson.toJson(currentGrid.matrix, writer);
                System.out.println("I evolved");
            }
        }
    }
}
