package org.example;

import lombok.Getter;

@Getter
public abstract class GridAbstract<TCellMatrix, TStateMatrix> {


    protected FinishStatus finishStatus = FinishStatus.NOT_FINISHED;

    protected TCellMatrix matrix;  // Cell matrix of N dimensions
    protected int m;  // The matrix size is m^N
    protected int r;  // Radius to initialize
    protected double initializationPercentage;
    protected boolean randomInitialConditions;
    protected int aliveCells;
    protected int aliveCellsPastState;

    public GridAbstract(int m, int r, double initializationPercentage, boolean randomInitialConditions) {
        this.m = m;
        this.r = r;
        this.initializationPercentage = initializationPercentage;
        this.randomInitialConditions = randomInitialConditions;
        this.matrix = getEmptyMatrix();
        this.aliveCells = 0;
        this.aliveCellsPastState = 0;

        this.initializeMatrix();
    }

    public abstract TStateMatrix cloneState();
    public GridState<TStateMatrix> getCurrentGridState() {
        TStateMatrix stateMatrix = cloneState();
        return new GridState<>(stateMatrix, this.aliveCells, this.getBiggestDistanceFromCenter(stateMatrix));
    }
    public abstract double getBiggestDistanceFromCenter(TStateMatrix matrix);
    public abstract GridState<TStateMatrix> evolve(int amountToRevive, int neighboursToDie1, int neighboursToDie2);
    public abstract boolean isFinished();

    // Generate a matrix of cells of N dimensions
    protected abstract TCellMatrix getEmptyMatrix();

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
