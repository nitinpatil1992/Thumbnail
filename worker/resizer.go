package main

import (
	"fmt"

	"gopkg.in/gographics/imagick.v2/imagick"
)

func Resizer(imagePath, thumbnailPath string, thumbnilHeight, thumbnilWidth uint) error {

	imagick.Initialize()
	defer imagick.Terminate()

	var err error
	mw := imagick.NewMagickWand()

	err = mw.ReadImage(imagePath)
	if err != nil {
		fmt.Printf("Error while reading file %s with :", imagePath, err)
		return err
	}

	// The blur factor is a float, where > 1 is blurry, < 1 is sharp
	err = mw.ResizeImage(thumbnilHeight, thumbnilWidth, imagick.FILTER_LANCZOS, 1)
	if err != nil {
		fmt.Printf("Error while resizing image : %v", err)
		return err
	}

	// Set the compression quality to 95 (high quality = low compression)
	err = mw.SetImageCompressionQuality(95)
	if err != nil {
		fmt.Printf("Error while setting image quality : %v", err)
		return err
	}

	err = mw.WriteImage(thumbnailPath)
	if err != nil {
		fmt.Printf("Error while writting thumbnail with : %v", err)
		return err
	}

	fmt.Printf("Wrote: %s\n", thumbnailPath)
	return nil
}
