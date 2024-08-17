package org.example;

import lombok.Getter;

import java.util.stream.IntStream;

@Getter
public class Grid2D extends GridAbstract<Cell[][]> {
    public Grid2D(int m, int r, double initializationPercentage, boolean randomInitialConditions) {
        super(m, r, initializationPercentage, randomInitialConditions);
    }


    @Override
    protected Cell[][] getEmptyMatrix() {
        Cell[][] newMatrix = new Cell[m][m];
        IntStream.range(0, m).forEach(i -> IntStream.range(0, m).forEach(j -> newMatrix[i][j] = new Cell()));
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
    public Cell[][] cloneState() {
        Cell[][] matrixClone = new Cell[m][m];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                matrixClone[i][j] = this.matrix[i][j].cloneState();
            }
        }
        return matrixClone;
    }

    @Override
    public void evolve() {
        //Como necesito comparar contra los estados en t-1 cuando paso al estado t primero realizo una copia de la matriz
        Cell[][] auxMatrix = cloneState();
        //Ahora que tengo esto, puede empezar a generar la matriz en tiempo t comparando cada celda contra sus vecinos en el tiempo t-1
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < m; j++) {
                int aliveCount = neighbourCount(i, j, auxMatrix);
                //Si esta viva y no tiene 2 o 3 vecinos vivos, muere
                if(matrix[i][j].isState() && !(aliveCount==2 || aliveCount==3)){
                    matrix[i][j].switchState();
                } else if (!matrix[i][j].isState() && aliveCount==3) { //Si esta muerta y tienen 3 vecinos vivos, revive
                    matrix[i][j].switchState();
                }
            }
        }
    }

    @Override
    public boolean isFinished() {
        for (int i = 0; i < m; i++) {
            //reviso los bordes para ver si alguna celda esta prendida
            if(matrix[0][i].isState() || matrix[m-1][i].isState() || matrix[i][0].isState() ||matrix[i][m-1].isState()){
                return true;
            }
        }
        return false;
    }
    
    // funcion que cuenta la cantidad de vecinos vivos que tiene la celda 
    private int neighbourCount(int row, int col, Cell[][] auxMatrix) {
        int aliveCount = 0;

        for (int i = row-1; i <= row+1; i++) {
            if(i>=0 && i<m) {
                for (int j = col - 1; j <= col + 1; j++) {
                    if(j>=0 && j<m) {
                        aliveCount += (auxMatrix[i][j].isState()) ? 1 : 0;
                    }
                }
            }
        }

        return aliveCount;
    }
}
