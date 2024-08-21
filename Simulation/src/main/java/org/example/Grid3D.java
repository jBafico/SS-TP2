package org.example;

import java.util.stream.IntStream;

public class Grid3D extends GridAbstract<Cell[][][], Boolean[][][]>{


    Boolean[][][] pastState;
    public Grid3D(int m, int r, double initializationPercentage, boolean randomInitialConditions) {
        super(m, r, initializationPercentage, randomInitialConditions);
        pastState = new Boolean[m][m][m];
    }

    @Override
    public Boolean[][][] cloneState() {
        Boolean[][][] matrixClone = new Boolean[m][m][m];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                for (int k = 0; k < m; k++) {
                    matrixClone[i][j][k] = this.matrix[i][j][k].isAlive();
                }
            }
        }
        return matrixClone;
    }

    @Override
    public Boolean[][][] evolve(int amountToRevive, int neighboursToDie1, int neighboursToDie2) {
        //Como necesito comparar contra los estados en t-1 cuando paso al estado t primero realizo una copia de la matriz
        pastState = cloneState();
        aliveCellsPastState=aliveCells;
        //Ahora que tengo esto, puede empezar a generar la matriz en tiempo t comparando cada celda contra sus vecinos en el tiempo t-1
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                for (int k = 0; k < m; k++) {
                    int aliveCount = neighbourCount(i, j, k, pastState);
                    //Si esta viva y no tiene 2 o 3 vecinos vivos, muere
                    if(matrix[i][j][k].isAlive() && !(aliveCount==neighboursToDie1 || aliveCount==neighboursToDie2)){
                        matrix[i][j][k].switchState();
                        aliveCells--;
                    } else if (!matrix[i][j][k].isAlive() && aliveCount==amountToRevive) { //Si esta muerta y tienen 3 vecinos vivos, revive
                        matrix[i][j][k].switchState();
                        aliveCells++;
                    }
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
            for (int j = 0; j < m; j++) {
                for (int k = 0; k < m; k++) {
                    if (i == 0 || i == m-1 || j == 0 || j == m-1 || k == 0 || k == m-1) {
                        if (matrix[i][j][k].isAlive()) {
                            // The border has been reached -> simulation finished
                            finishStatus = FinishStatus.WITH_BORDER;
                            return true;
                        }
                    }
                }
            }
        }

        return false;
    }

    @Override
    protected Cell[][][] getEmptyMatrix() {
        Cell[][][] newMatrix = new Cell[m][m][m];
        IntStream.range(0, m)
                .forEach(i -> IntStream.range(0, m)
                        .forEach(j -> IntStream.range(0, m)
                                .forEach(k -> newMatrix[i][j][k] = new Cell(false))));
        return newMatrix;
    }

    @Override
    protected void initializeMatrixWithRandomValues() {
        int middle = m / 2;
        for (int i = -r; i <= r; i++) {
            for (int j = -r; j <= r; j++) {
                for (int k = -r; k <= r; k++) {
                    int x = middle + i;
                    int y = middle + j;
                    int z = middle + k;
                    if (x >= 0 && x < m && y >= 0 && y < m && z >= 0 && z < m) { // border check
                        if (Math.random() <= initializationPercentage) {
                            matrix[x][y][z].setAlive();
                            aliveCells++;
                        }
                    }

                }
            }
        }
    }

    @Override
    protected void initializeMatrixWithGivenValues() {
        // todo initialize the matrix with values from initialization.json file
    }


    private int neighbourCount(int x, int y, int z, Boolean[][][] auxMatrix) {
        int aliveCount = 0;

        for (int i = x-1; i <= x+1; i++) {
            if (i < 0 || i >= m){
                continue;
            }
            for (int j = y - 1; j <= y + 1; j++) {
                if (j < 0 || j >= m){
                    continue;
                }
                for (int k = z - 1; k <= z + 1; k++) {
                    if (k < 0 || k >= m){
                        continue;
                    }
                    if(!(i==x && j==y && k==z)){ //we dont want to consider the cell we are analizing
                        aliveCount = aliveCount + ( (auxMatrix[i][j][k]) ? 1 : 0);
                    }

                }
            }
        }

        return aliveCount;
    }

    private boolean compareStates(){
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                for (int k = 0; k < m; k++) {
                    if (matrix[i][j][k].isAlive() != pastState[i][j][k]) {
                        return false;
                    }
                }
            }
        }
        return true;
    }

}
