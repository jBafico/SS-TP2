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
        //TODO SACAR HISTORY Y VER COMO ESCRIBIR EL JSON DINAMICAMENTE CON EL FORMATO CORRECTO
        List<Boolean[][]> history = new ArrayList<>();
        ObjectMapper mapper = new ObjectMapper();


            System.out.println("Simulation started");
            while (!currentGrid.isFinished()) {
                history.add(currentGrid.cloneState());
                currentGrid.evolve();
                System.out.println("I evolved");
            }
            try (FileWriter writer = new FileWriter("../files/simulationOutput.json")) {
                mapper.writeValue(writer, history);
            }

    }
    
}
