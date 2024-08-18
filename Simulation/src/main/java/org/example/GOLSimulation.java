package org.example;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

//For keeping history

@Getter
@RequiredArgsConstructor
public class GOLSimulation<TMatrix, TState> {
    private final GridAbstract<TMatrix, TState> currentGrid;

    public void start(String fileOutputName) throws IOException {
        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        int evolutions = 0;

        try (FileWriter writer = new FileWriter("../files/%s".formatted(fileOutputName))) {
            System.out.println("Simulation started");

            writer.write("[\n");

            while (!currentGrid.isFinished()) {
                var matrix = currentGrid.evolve();

                var mapToJson = Map.of("evolution_%s".formatted(evolutions),matrix);


                gson.toJson(mapToJson, writer);
                writer.write(",\n");

                System.out.printf("I evolved %d times \n", ++evolutions);
            }

            gson.toJson(Map.of("evolution_%s".formatted(evolutions),currentGrid.cloneState()), writer);

            writer.write("\n]");
        }
    }
}
