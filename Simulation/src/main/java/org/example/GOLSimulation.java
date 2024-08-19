package org.example;

import java.io.FileWriter;
import java.io.IOException;
import java.util.Map;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.example.records.AllSimulationParams;
import org.example.records.SingleSimulationParams;

//For keeping history

@Getter
@RequiredArgsConstructor
public class GOLSimulation<TMatrix, TState> {
    private final GridAbstract<TMatrix, TState> currentGrid;
    private final SingleSimulationParams params;

    public void start(FileWriter writer) throws IOException {
        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        int evolutions = 0;

        System.out.println("Simulation started");

        writer.write("\"params\": ");
        gson.toJson(params, writer);
        writer.write(",\n\"results\": [\n");

        while (!currentGrid.isFinished() && evolutions < params.maxEpochs()) {
            var matrix = currentGrid.evolve(params.ruleset().amountToRevive(), params.ruleset().neighboursToDie1(), params.ruleset().neighboursToDie2());

            var mapToJson = Map.of("evolution_%s".formatted(evolutions),matrix);


            gson.toJson(mapToJson, writer);
            writer.write(",\n");

            System.out.printf("I evolved %d times \n", ++evolutions);
        }

        gson.toJson(Map.of("evolution_%s".formatted(evolutions),currentGrid.cloneState()), writer);

        writer.write("\n]");
    }
}

