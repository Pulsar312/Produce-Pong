FROM python:3.8

# Set the home directory to /root
ENV HOME /root
# cd into the home directory
WORKDIR /root

# Copy all app files into the image
COPY . .

#add all dependencies from requirements file
RUN pip3 install -r requirements.txt

# Allow port 8080 to be accessed
# from outside the container
EXPOSE 8080

# For the database, this helps it wait until database loads
# Citation: This solution has been a reccomendation from Professor Jesse Hartloff, in his CSE 312 class at UB.
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

# Wait for database, and run the app
CMD /wait && python3 app.py