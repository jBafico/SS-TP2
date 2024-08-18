package org.example;

import lombok.Getter;

import java.util.stream.IntStream;

@Getter
public class Grid2D extends GridAbstract<Cell[][], Boolean[][]> {
    public Grid2D(int m, int r, double initializationPercentage, boolean randomInitialConditions) {
        super(m, r, initializationPercentage, randomInitialConditions);
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
    public Boolean[][] evolve() {
        //Como necesito comparar contra los estados en t-1 cuando paso al estado t primero realizo una copia de la matriz
        Boolean[][] auxMatrix = cloneState();
        //Ahora que tengo esto, puede empezar a generar la matriz en tiempo t comparando cada celda contra sus vecinos en el tiempo t-1
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                int aliveCount = neighbourCount(i, j, auxMatrix);
                //Si esta viva y no tiene 2 o 3 vecinos vivos, muere
                if(matrix[i][j].isAlive() && !(aliveCount==2 || aliveCount==3)){
                    matrix[i][j].switchState();
                } else if (!matrix[i][j].isAlive() && aliveCount==3) { //Si esta muerta y tienen 3 vecinos vivos, revive
                    matrix[i][j].switchState();
                }
            }
        }
        return auxMatrix;
    }



    @Override
    public boolean isFinished() {
        // Check if border has been reached by an alive cell
        for (int i = 0; i < m; i++) {
            if(matrix[0][i].isAlive() || matrix[m-1][i].isAlive() || matrix[i][0].isAlive() ||matrix[i][m-1].isAlive()){
                // The border has been reached -> simulation finished
                return true;
            }
        }

        // Check if there is at least one alive cell
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                if (matrix[i][j].isAlive()) {
                    // At least one cell is alive -> simulation not finished yet
                    return false;
                }
            }
        }

        // No alive cells found -> simulation finished
        return true;
    }
    
    // funcion que cuenta la cantidad de vecinos vivos que tiene la celda
    private int neighbourCount(int row, int col, Boolean[][] auxMatrix) {
        int aliveCount = 0;

        for (int i = row-1; i <= row+1; i++) {
            if(i>=0 && i<m) {
                for (int j = col - 1; j <= col + 1; j++) {
                    if(j>=0 && j<m) {
                        aliveCount = aliveCount + ( (auxMatrix[i][j]) ? 1 : 0);
                    }
                }
            }
        }
        return aliveCount;
    }
}
