package org.example;

import lombok.Getter;

import java.util.stream.IntStream;

@Getter
public class Grid2D extends GridAbstract<Cell[][], Boolean[][]> {

    Boolean[][] pastState;

    public Grid2D(int m, int r, double initializationPercentage, boolean randomInitialConditions) {
        super(m, r, initializationPercentage, randomInitialConditions);
        pastState = new Boolean[m][m];
    }


    @Override
    protected Cell[][] getEmptyMatrix() {
        Cell[][] newMatrix = new Cell[m][m];
        IntStream.range(0, m).forEach(i -> IntStream.range(0, m).forEach(j -> newMatrix[i][j] = new Cell(false)));
        return newMatrix;
    }

    @Override
    protected void initializeMatrixWithRandomValues() {
        int middle = m / 2;
        for (int i = -r; i <= r; i++) {
            for (int j = -r; j <= r; j++) {
                int x = middle + i;
                int y = middle + j;
                if (x >= 0 && x < m && y >= 0 && y < m) { // border check
                    if (Math.random() <= initializationPercentage) {
                        matrix[x][y].setAlive();
                        aliveCells++;
                    }
                }
            }
        }
    }

    @Override
    protected void initializeMatrixWithGivenValues() {
        // todo initialize the matrix with values from initialization.json file
    }

    @Override
    public Boolean[][] cloneState() {
        Boolean[][] matrixClone = new Boolean[m][m];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                matrixClone[i][j] = this.matrix[i][j].isAlive();
            }
        }
        return matrixClone;
    }


    // Returns previous state on evolution
    @Override
    public Boolean[][] evolve(int amountToRevive, int neighboursToDie1, int neighboursToDie2) {
        //Como necesito comparar contra los estados en t-1 cuando paso al estado t primero realizo una copia de la matriz
        pastState = cloneState();
        aliveCellsPastState=aliveCells;
        //Ahora que tengo esto, puede empezar a generar la matriz en tiempo t comparando cada celda contra sus vecinos en el tiempo t-1
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                int aliveCount = neighbourCount(i, j, pastState);
                //Si esta viva y no tiene 2 o 3 vecinos vivos, muere
                if(matrix[i][j].isAlive() && !(aliveCount==neighboursToDie1 || aliveCount==neighboursToDie2)){
                    matrix[i][j].switchState();
                    aliveCells--;
                } else if (!matrix[i][j].isAlive() && aliveCount==amountToRevive) { //Si esta muerta y tienen 3 vecinos vivos, revive
                    matrix[i][j].switchState();
                    aliveCells++;
                }
            }
        }
        return pastState;
    }



    @Override
    public boolean isFinished() {
        //if there are no alive cells -> simulation finished
        if(aliveCells==0){
            finishStatus = FinishStatus.WITH_ALL_DEAD;
            return true;
        }

        //if the matrix is equal to its past state -> simulation finished
        if(aliveCellsPastState==aliveCells && compareStates()){
            finishStatus = FinishStatus.WITH_SAME_AS_PREVIOUS_STATE;
            return true;
        }

        // Check if border has been reached by an alive cell
        for (int i = 0; i < m; i++) {
            if(matrix[0][i].isAlive() || matrix[m-1][i].isAlive() || matrix[i][0].isAlive() ||matrix[i][m-1].isAlive()){
                // The border has been reached -> simulation finished
                finishStatus = FinishStatus.WITH_BORDER;
                return true;
            }
        }

        return false;
    }
    
    // funcion que cuenta la cantidad de vecinos vivos que tiene la celda
    private int neighbourCount(int row, int col, Boolean[][] auxMatrix) {
        int aliveCount = 0;

        for (int i = row-1; i <= row+1; i++) {
            if(i>=0 && i<m) {
                for (int j = col - 1; j <= col + 1; j++) {
                    if(j>=0 && j<m) {
                        if(!(i==row && j==col)){ //we dont want to consider the cell we are analizing
                            aliveCount = aliveCount + ( (auxMatrix[i][j]) ? 1 : 0);
                        }
                    }
                }
            }
        }
        return aliveCount;
    }

    private boolean compareStates(){
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                if (matrix[i][j].isAlive() != pastState[i][j]) {
                    return false;
                }
            }
        }
        return true;
    }
}
