{
  data.map((project) => <Cell data={project} key={project.title} />);
}

<img src={allMaps["img1.png"]} />
<img src={allMaps["img2.png"]} />
<img src={allMaps["img3.png"]} />
<img src={allMaps["img4.png"]} />

<div>
{
      listOfImages.map(
        (image, index) =>    <img key={index} src={image} alt="info"></img>
      )
}
</div>

{allMaps.map((image, index) => (
    <img key={index} src={image} alt="info"></img>
  ))}