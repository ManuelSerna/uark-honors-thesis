//***********************************************
// Dynamic Time Warping
//***********************************************
#include <iostream>
#include <cmath>
using namespace std;

#define N 10
#define INFTY 999999

// Print matrix for debugging
void printMatrix(int a[N+1][N+1])
{
    for(int x = 0; x < N+1; x++)
    {
        cout << "\t|";
        
        for(int y = 0; y < N+1; y++)
        {
            cout << a[x][y] << "|";
        }
        
        cout << endl;
    }
}

// Compute distance
int distance(int a, int b)
{
    return abs(a - b);
}

// Get minimum value
int min(int a, int b)
{
    if(a <= b)
    {
        return a;
    }
    else
    {
        return b;
    }
}

// Find minimum distance to align two time series s and t
int dtw(int s[], int t[])
{
    // Have D be a (n+1)x(n+1) matrix so we can have s and t's elements as the initial values
    int D[N+1][N+1];
    
    for(int i = 0; i < N; i++)
    {
        D[i+1][0] = s[i];
    }
    
    for(int j = 0; j < N; j++)
    {
        D[0][j+1] = t[j];
    }
    
    for(int i = 1; i < N; i++)
    {
        for(int j = 1; j < N; j++)
        {
            D[i][j] = INFTY;
        }
    }
    
    D[0][0] = D[1][1] = 0;
    
    // Calculate minimum distance, which will be D[N][N]
    for(int i = 1; i < N+1; i++)
    {
        for(int j = 1; j < N+1; j++)
        {
            int d = distance(D[i][0], D[0][j]);// (s[i], t[j])
            D[i][j] = d + min(D[i-1][j],     // insertion
                          min(D[i][j-1],     // deletion
                              D[i-1][j-1])); // match
        }
    }
    
    //printMatrix(D);
    
    return D[N][N];
}

int main()
{
    // Random input, assume s and t to be the same length
    int s[N] = {1, 3, 4, 9, 8, 2, 1, 5, 7, 3};
    int t[N] = {1, 6, 2, 3, 0, 9, 4, 3, 6, 3};
    
    int minDistance = dtw(s, t);
    
    cout << "Minimum distance with given data: " << minDistance << endl;
    
    return 0;
}
