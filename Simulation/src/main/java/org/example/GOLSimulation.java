package org.example;

import java.io.FileWriter;
import java.io.IOException;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import org.example.records.SingleSimulationParams;

//For keeping history

@Getter
@RequiredArgsConstructor
public class GOLSimulation<TCellMatrix, TStateMatrix> {
    private final GridAbstract<TCellMatrix, TStateMatrix> currentGrid;
    private final SingleSimulationParams params;

    public void start(FileWriter writer) throws IOException {
        Gson gson = new GsonBuilder().setPrettyPrinting().create();
        int evolutions = 0;
        writer.write("{\n\"params\": ");
        gson.toJson(params, writer);
        writer.write(",\n\"results\": {\n");


        //para calcular la distancia
        double averageBiggestRadiusDistance = 0;
        //

        while (!currentGrid.isFinished() && evolutions < params.maxEpochs()) {
            var gridState = currentGrid.evolve(params.ruleset().amountToRevive(), params.ruleset().neighboursToDie1(), params.ruleset().neighboursToDie2());

            averageBiggestRadiusDistance += gridState.biggestDistanceFromCenter();
            writer.write("\"evolution_%s\": ".formatted(evolutions));
            gson.toJson(gridState, writer);
            writer.write(",\n");

            evolutions++;
            if (evolutions % 10 == 0) {
                System.out.printf("I evolved %d times \n", evolutions);
            }
        }
        System.out.printf("Total evolutions: %d\n\n\n", evolutions);

        writer.write("\"evolution_%s\": ".formatted(evolutions));
        gson.toJson(currentGrid.getCurrentGridState(), writer);


        FinishStatus finalStatus = evolutions == params.maxEpochs() ? FinishStatus.WITH_MAX_EPOCHS: currentGrid.getFinishStatus();

        writer.write("\n}, \"endingStatus\": \"%s\", \"averageBiggestRadiusDistance\": %s \n}".formatted(finalStatus.getStatus(), averageBiggestRadiusDistance / evolutions));
    }
}

