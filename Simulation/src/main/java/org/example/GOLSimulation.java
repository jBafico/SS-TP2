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

        writer.write("{\n\"params\": ");
        gson.toJson(params, writer);
        writer.write(",\n\"results\": {\n");

        while (!currentGrid.isFinished() && evolutions < params.maxEpochs()) {
            var matrix = currentGrid.evolve(params.ruleset().amountToRevive(), params.ruleset().neighboursToDie1(), params.ruleset().neighboursToDie2());

            writer.write("\"evolution_%s\": ".formatted(evolutions));
            gson.toJson(matrix, writer);
            writer.write(",\n");

            evolutions++;
            if (evolutions % 10 == 0) {
                System.out.printf("I evolved %d times \n", evolutions);
            }
        }

        System.out.printf("Total evolutions: %d\n\n\n", evolutions);

        writer.write("\"evolution_%s\": ".formatted(evolutions));
        gson.toJson(currentGrid.cloneState(), writer);

        writer.write("\n}\n}");
    }
}

