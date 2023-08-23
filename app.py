from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")

@app.route("/crypto")
def crypto():
    return render_template("crypto.html")

@app.route("/swimming")
def swimming():
    return render_template("swimming.html")

@app.route("/powerlifting")
def powerlifting():
    return render_template("powerlifting.html")

@app.route("/crypto/ca_ss", methods = ["POST", "GET"])
def ca_ss():
    if request.method == "GET":
        return render_template("ca_ss.html")
    
    import math
    from cumulative_array_ss import setup, is_prime

    error = None

    try:
        n = int(request.form['n'])
        t = int(request.form['t'])
        s = int(request.form['s'])
        p = int(request.form['p'])

        p_minimun = math.comb(int(n), int(t) - 1)

        if p <= n or p <= s or p_minimun > p or t > n or not is_prime(p) or t <= 0 or n <= 0 or p <= 0 or int(t) != t or int(n) != n or int(p) != p:
            if not is_prime(p) or p <= s or p_minimun > p: error = "P needs to be a prime number and bigger than s and nC(t-1)."
            elif t > n: error = "Please input t < n"
            else: error = "Please input positive integers."

            return render_template('ca_ss.html', error=error)
        
        shares = setup(s, t, n, p)
        no = math.comb(int(n) - 1, int(t) - 1)
        return render_template("ca_result.html", participants=shares, t=t, n=n, p=p, s=s, total=p_minimun, no=no, number=no)
        
    except ValueError:
        error = "Invalid input format. Please enter a positive integer."
        return render_template('ca_ss.html', error = error) 

@app.route('/crypto/ca_ss/ca_process_shares', methods=["POST"])
def ca_process_shares():
    import ast, math

    n = int(request.form.get("n"))
    t = int(request.form.get("t"))
    p = int(request.form.get("p"))
    s = int(request.form.get("s"))
    shares = request.form.get("shares")
    shares = ast.literal_eval(shares)

    p_minimun = math.comb(int(n), int(t) - 1)
    no = math.comb(int(n) - 1, int(t) - 1)

    from cumulative_array_ss import reconstruct, is_positive_integer

    try:

        total_shares = []

        # Iterate through the form fields to retrieve x and y values
        for i in range(t):
            share = []

            for j in range(1, math.comb(int(n) - 1, int(t) - 1) + 1):

                x_field = f'x_value{j * i + j}'
                y_field = f'y_value{j * i + j}'

                # Retrieve x and y values from the form
                x = request.form[x_field]
                y = request.form[y_field]

                if x and y and is_positive_integer(x) and is_positive_integer(y):
                    share.append([int(x), int(y)])
                else:
                    error = "Invalid input format. Please enter positive integers and fill out the all fields."
                    return render_template("ca_result.html", participants=shares, t=t, n=n, p=p, s=s, total=p_minimun, no=no, error=error, number=no)
                
                total_shares.append(share)
            
        key = reconstruct(total_shares, p)

        if key != s:
            error = "Failed to recover secret maybe due to wrong shares inputted."
            return render_template("ca_result.html", participants=shares, t=t, n=n, p=p, s=s, total=p_minimun, no=no, error=error)
        else:
            return render_template("congrats.html", key=key)

        
    except ValueError:
        error = "Invalid input format. Please enter a positive integer."
        return render_template("ca_result.html", participants=shares, t=t, n=n, p=p, s=s, total=p_minimun, no=no, error=error, number=no)

@app.route("/crypto/sss", methods = ["POST", "GET"])
def sss():
    if request.method == "GET":
        return render_template("sss.html")
    
    import shamir_ss

    error = None

    try:
        n = int(request.form['n'])
        t = int(request.form['t'])
        s = int(request.form['s'])
        p = int(request.form['p'])

        if p <= n or p <= s or n < t or not shamir_ss.is_prime(p) or t <= 0 or n <= 0 or p <= 0 or int(t) != t or int(n) != n or int(p) != p:
            if not shamir_ss.is_prime(p) or p <= s: error = "P needs to be a prime number and bigger than s and n."
            elif t > n: error = "Please input t < n"
            else: error = "Please input positive integers."

            return render_template('sss.html', error=error)
        
        shares = shamir_ss.generate(s, t, n, p)
        return render_template("result.html", shares=shares, t=t, n=n, p=p, s=s)
        
    except ValueError:
        error = "Invalid input format. Please enter a positive integer."
        return render_template('sss.html', error = error) 

@app.route('/crypto/sss/process_shares', methods=["POST"])
def process_shares():
    import ast

    n = int(request.form.get("n"))
    t = int(request.form.get("t"))
    p = int(request.form.get("p"))
    s = int(request.form.get("s"))
    shares = request.form.get("shares")
    shares = ast.literal_eval(shares)
    import shamir_ss
    try:
        x_values = []
        y_values = []

        # Iterate through the form fields to retrieve x and y values
        for i in range(t):
            x_field = f'x_value{i}'
            y_field = f'y_value{i}'

            # Retrieve x and y values from the form
            x = request.form[x_field]
            y = request.form[y_field]

            if x and y and shamir_ss.is_positive_integer(x) and shamir_ss.is_positive_integer(y):
                x_values.append(int(x))
                y_values.append(int(y))
            else:
                error = "Invalid input format. Please enter positive integers and fill out the all fields."
                return render_template("result.html", shares=shares, t=t, n=n, p=p, s=s, error=error) 
            
        key = shamir_ss.interpolate(x_values, y_values, p)

        if key != s:
            error = "Failed to recover secret maybe due to wrong shares inputted."
            return render_template("result.html", shares=shares, t=t, n=n, p=p, s=s, error=error)
        else:
            return render_template("congrats.html", key=key)

        
    except ValueError:
        error = "Invalid input format. Please enter a positive integer."
        return render_template("result.html", shares=shares, t=t, n=n, p=p, s=s, error=error)

@app.route('/crypto/ssef_project')
def ssef_project():

    return render_template('ssef_project.html')

if __name__ == '__main__':
    app.run()