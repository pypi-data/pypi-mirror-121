import time

def _fib(n, div):
    if n <= 0:
	    return (0, 1)
    else:
        a, b = _fib(n // 2, div)
        c = (a * (b * 2 - a))%div
        d = (a*a + b*b)%div
        if n % 2 == 0:
            return (c, d)
        else:
            return (d, (c + d)%div)

#Main:
def main():
    print("In each test case, chose a number 'a', a number 'b' such that b >= a, and a number 'd'.")
    print("The computer will tell you the remainder of F(a) + F(a+1) + ... + F(b) by d, where F(n) is the nth Fibonacci number.")
    print("Note: F(0)=0, F(1)=1, ...")

    while True:
        print("Enter 'a', 'b' and 'd' separated by a space:")
        a,b,d = [int(c) for c in input().split()]
        t1 = time.perf_counter_ns()
        if a == 0:
            s = (list(_fib(b+2,d))[0]-1)%d
        else:
            l = list(_fib(a-1,d))
            m = list(_fib(b-a+2,d))
            s = ((l[1]*(m[1]-1))%d + (l[0]*(m[0]-1))%d)%d
        t2 = time.perf_counter_ns()

        print("F_" + str(a) + " + ... + F_" + str(b) + " has a remainder of " + str(s) + " when divided by " + str(d))
        print("Time Elapsed (nanoseconds): " + str(t2 - t1))
        if input("Do you want to make another test? (y/n): ") == "n":
            break

    print("Goodbye!")

main()
