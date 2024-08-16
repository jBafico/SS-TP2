package org.example;

import java.util.LinkedList;
import java.util.List;

import lombok.Getter;
import lombok.RequiredArgsConstructor;

//For keeping history

@Getter
@RequiredArgsConstructor
public class GOLSimulation<TMatrix> {


    private final GridAbstract<TMatrix> currentGrid;
    private List<TMatrix> history = new LinkedList<>();


    public void start(){
        history.add(currentGrid.cloneState());
        while (!currentGrid.isFinished()) {
            currentGrid.evolve();
            history.add(currentGrid.cloneState());
        }
        history.add(currentGrid.cloneState());
    }




    
}
