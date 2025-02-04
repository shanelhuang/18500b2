import React from "react";
import { Link } from "react-router-dom";
import Helmet from "react-helmet";
import Main from "../layouts/Main";
import Cell from "../components/Projects/Cell";
import data from "../data/projects";

/* dynamically import all images from a directory - using webpack */
function importAll(r) {
  let images = {};
  r.keys().map((item, index) => {
    images[item.replace("./", "")] = r(item);
  });
  return images;
}

const allMaps = importAll(
  require.context("../../public/images/mapImages", false, /\.(png|jpe?g|svg)$/)
);

const Projects = () => (
  <Main>
    {" "}
    <Helmet title="Visualize" />
    <article className="post" id="projects">
      <header>
        <div className="title">
          <h2>
            <Link to="/projects">Visualize</Link>
          </h2>
          <p>These are indoor maps generated by RIP.</p>
        </div>
      </header>
      <img src={allMaps["img1.png"]} />
      <img src={allMaps["img2.png"]} />
      <img src={allMaps["img3.png"]} />
      <img src={allMaps["img4.png"]} />
    </article>
  </Main>
);

export default Projects;
