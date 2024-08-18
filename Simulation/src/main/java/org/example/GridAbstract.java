package org.example;

import lombok.Getter;

@Getter
public abstract class GridAbstract<TMatrix, TState> {
    protected TMatrix matrix;  // Cell matrix of N dimensions
    protected int m;  // The matrix size is m^N
    protected int r;  // Radius to initialize
    protected double initializationPercentage;
    protected boolean randomInitialConditions;
    protected int aliveCells;

    public GridAbstract(int m, int r, double initializationPercentage, boolean randomInitialConditions) {
        this.m = m;
        this.r = r;
        this.initializationPercentage = initializationPercentage;
        this.randomInitialConditions = randomInitialConditions;
        this.matrix = getEmptyMatrix();
        this.aliveCells = 0;

        this.initializeMatrix();
    }

    public abstract TState cloneState();
    public abstract TState evolve();
    public abstract boolean isFinished();

    // Generate a matrix of cells of N dimensions
    protected abstract TMatrix getEmptyMatrix();

    // Initialize the matrix with random values
    protected abstract void initializeMatrixWithRandomValues();

    // Initialize the matrix with given values
    protected abstract void initializeMatrixWithGivenValues();

    private void initializeMatrix(){
        if (randomInitialConditions) {
            initializeMatrixWithRandomValues();
        } else {
            initializeMatrixWithGivenValues();
        }
    }


}
