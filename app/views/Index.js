import React from "react";
import { Link } from "react-router-dom";

import Main from "../layouts/Main";

const Index = () => (
  <Main>
    <article className="post" id="index">
      <header>
        <div className="title">
          <h2>
            <Link to="/">RIP: Robotic Indoor Plotting</Link>
          </h2>
          <p>Introduction and Project Summary</p>
        </div>
      </header>
      <p>
        {" "}
        Google Maps lacks accurate and comprehensive indoor positioning
        information. Businesses and establishments that upload their own floor
        plans are able to show specific details on indoor locations. However,
        most buildings do not have this information available online, making it
        difficult for visitors to navigate indoors.
      </p>
      <p>
        The Robotic Indoor Plotting project will autonomously generate indoor
        floor plans, while labeling room descriptors and dimensions. When placed
        indoors, the robot will explore the space, creating a 2D map using
        built-in obstacle detection sensors and an external scanning Lidar
        sensor. After traversing the indoor space, the robot will synthesize
        information into a readable format for the user to analyze on a web
        application. Since the data will be stored, the user can perform
        repeated scans more efficiently to update indoor positioning in the
        future.
      </p>
      <p>
        {" "}
        See this in action{" "}
        <a
          href="http://course.ece.cmu.edu/~ece500/projects/s20-teamb2/"
          // TODO: eventually have this link to demo video
        >
          here
        </a>
        .
      </p>
    </article>
  </Main>
);

export default Index;
