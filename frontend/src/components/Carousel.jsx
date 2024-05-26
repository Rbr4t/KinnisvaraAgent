import React, { useState, useEffect, useRef } from "react";
import { Box, Typography, Paper } from "@mui/material";
import { styled } from "@mui/system";

const CarouselContainer = styled(Box)({
  position: "relative",
  width: "100%",
  overflow: "hidden",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
  marginTop: "20px",
});

const CarouselWrapper = styled(Box)({
  display: "flex",
  transition: "transform 0.5s ease-in-out",
  width: "99%",
});

const FeaturePaper = styled(Paper)({
  minWidth: "100%",
  padding: "20px",
  textAlign: "center",
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
});

const Carousel = ({ features }) => {
  const [currentIndex, setCurrentIndex] = useState(features.length);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const carouselRef = useRef();

  const totalSlides = features.length;
  const extendedFeatures = [...features, ...features, ...features];

  const handleNext = () => {
    setIsTransitioning(true);
    setCurrentIndex((prevIndex) => prevIndex + 1);
  };

  useEffect(() => {
    const interval = setInterval(() => {
      handleNext();
    }, 4000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (currentIndex >= totalSlides * 2) {
      setTimeout(() => {
        setIsTransitioning(false);
        setCurrentIndex(totalSlides);
        carouselRef.current.style.transition = "none";
        carouselRef.current.style.transform = `translateX(-${
          totalSlides * 100
        }%)`;
      }, 500);
    } else {
      carouselRef.current.style.transition = "transform 0.5s ease-in-out";
      carouselRef.current.style.transform = `translateX(-${
        currentIndex * 100
      }%)`;
    }
  }, [currentIndex, totalSlides]);

  useEffect(() => {
    if (!isTransitioning) {
      carouselRef.current.style.transition = "none";
    }
  }, [isTransitioning]);

  return (
    <CarouselContainer>
      <CarouselWrapper ref={carouselRef}>
        {extendedFeatures.map((feature, index) => (
          <FeaturePaper key={index} elevation={3}>
            <Typography variant="h5" component="h3" gutterBottom>
              {feature.title}
            </Typography>
            <Typography variant="body1">{feature.description}</Typography>
          </FeaturePaper>
        ))}
      </CarouselWrapper>
    </CarouselContainer>
  );
};

export default Carousel;
