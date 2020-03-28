import React from "react";
import { Link } from "react-router-dom";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

const Nav = () => (
  <section id="sidebar">
    <section id="intro">
      <Link to="/" className="logo">
        <img src={`${BASE_PATH}/images/me_icon.jpg`} alt="" />
      </Link>
      <header>
        <h2>Team B2</h2>
        <p>
          <a href="mailto:ahebbar@andrew.cmu.edu">Aditi Hebbar (ahebbar)</a>
        </p>
        <p>
          <a href="mailto:albai@andrew.cmu.edu">Alexander Bai (albai)</a>
        </p>
        <p>
          <a href="mailto:shanelh@andrew.cmu.edu">Shanel Huang (shanelh)</a>
        </p>
      </header>
    </section>

    <section className="blurb">
      <h2>About</h2>
      <p>
        This project was created as a part of Carnegie Mellon University&apos;s
        Spring 2020 iteration of the ECE Capstone Design course. For more
        information and updates, see the{" "}
        <a href="http://course.ece.cmu.edu/~ece500/projects/s20-teamb2/">
          project blog
        </a>
      </p>
    </section>
  </section>
);

export default Nav;
