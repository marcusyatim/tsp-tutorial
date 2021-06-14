# The Travelling Salesman Problem with Google's OR-Tools

> The Travelling Salesman Problem (also called the Travelling
> Salesperson Problem or TSP) asks the following question: "Given a list
> of cities and the distances between each pair of cities, what is the
> shortest possible route that visits each city exactly once and returns
> to the origin city?"
> -- Wikipedia

The TSP is a famous and intensively studied optimisation problem that has been around for over 90 years. It has a vast area of application, including those that one might expect in logistics and delivery services. Indeed, our modern era includes many of such companies, e.g. UPS, Amazon, etc. that make use of fully optimised TSP solutions (although strictly speaking, these companies would be looking at the Vehicle Routing Problem, a subset of TSP. The Vehicle Routing Problem aims to find a solution that involves a fleet of vehicles, something that we will not be looking at today).

Today, we will imagine that we are a startup food catering business. We will have a set of delivery destinations, made known to us prior to the day of delivery, so as to plan a route that starts from our kitchen depot, goes to each destination and ends back at the same kitchen depot. This route will be optimised to either be of shortest distance or shortest time duration required. We also only have one food delivery van. As such, we are only looking at a basic TSP and not the Vehicle Routing Problem.

Our goal for today will not be to formulate an optimisation algorithm for the TSP. There already exists many prebuilt solutions out there and as many a wise man once said (including my good friend Chong Ming Zhe): do not reinvent the wheel. One of these solutions is included in Google OR-Tools and hence, we will be using the latter to help us craft our food delivery system. We will also be using Google Maps API, specifically the Distance Matrix API, to make our solution more user-friendly and feature filled.

### Prerequisites

We will be coding entirely in Python, so knowledge in Python language is required. As mentioned earlier, we will not be looking to analyse the TSP algorithm and thus, knowledge in operations research or theoretical computer science is not needed.

Of course, we need a Google account for this tutorial and also a billing method to utilise the Google APIs. Do not worry about any billings as we will be sticking to the free tier and you will not be charged anything. However, Google still requires you to fill up a billing method regardless. Kids, ask your parents for permission first!

### Google OR-Tools

As mentioned above, Google OR-Tools has a library with functions that can help us to solve the TSP. In fact, there is even a handy example guide written by Google that we are going to reference closely and borrow the code from extensively : [https://developers.google.com/optimization/routing/tsp](https://developers.google.com/optimization/routing/tsp). First, have a read through of the “Example: Solving a TSP with OR-Tools” in the given link and you can stop just before “Example: drilling a circuit board”. Copy the code from “Complete programs” and paste it in a new Python script.

### Improvements on the code

This article would be pretty uninteresting if we were to leave it right here. Instead, lets add some improvements to the already very helpful guide provided by Google. One obvious improvement is nicely suggested in the guide itself: add Google Maps Distance Matrix implementation. We will then also add a few more improvements: 1) add travel time matrix implementation, 2) add the ability to receive terminal inputs and 3) make the terminal output more user-friendly.

### Google Maps Distance Matrix

To help us with this implementation, we are again going to refer to a handy guide written by Google @ [https://developers.google.com/optimization/routing/vrp#distance_matrix_api](https://developers.google.com/optimization/routing/vrp#distance_matrix_api).

The rest of the coding tutorial can be viewed on my [YouTube video](https://www.youtube.com/watch?v=frHYJ_Bg4S0&t=340s)!
