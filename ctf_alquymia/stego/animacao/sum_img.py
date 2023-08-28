import os
import cv2

def remove_black_bg(path):
	src = cv2.imread(path, 1)
	
	tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
	_,alpha = cv2.threshold(tmp,1,255,cv2.THRESH_BINARY)
	b, g, r = cv2.split(src)
	rgba = [b, g, r, alpha]

	gray = cv2.cvtColor(rgba, cv2.COLOR_BGR2GRAY)
	ret, thresh = cv2.threshold(gray, 20, 255, 0)

	return cv2.merge(rgba, 4)

def replace_black_bg_with_white(path):
	image = cv2.imread(path)
	# convert the input image to grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# apply thresholding to convert grayscale to binary image
	ret, thresh = cv2.threshold(gray, 20, 255, 0)

	return thresh

def combine_images(input_directory, output_path):
	image_paths = [os.path.join(input_directory, filename) for filename in os.listdir(input_directory) if filename.endswith(".png")]
	image_paths.sort()

	im1 = replace_black_bg_with_white(image_paths[primeira])

	im2 = replace_black_bg_with_white(image_paths[primeira+1])
	combined_image = cv2.add(im1, im2)

	cv2.imwrite(f"{output_path}", cv2.bitwise_not(combined_image))

	primeira = 0
	ultima = primeira+14
	while (primeira < len(image_paths)):
		print(primeira)

		im1 = replace_black_bg_with_white(image_paths[primeira])

		im2 = replace_black_bg_with_white(image_paths[primeira+1])
		combined_image = cv2.add(im1, im2)
		for i in image_paths[primeira+2:ultima]:
			im2 = replace_black_bg_with_white(i)
			combined_image = cv2.add(combined_image, im2)
		
		cv2.imwrite(f"grupos/{primeira}_{output_path}", cv2.bitwise_not(combined_image))

		primeira = ultima
		ultima = primeira+14

if __name__ == "__main__":
	input_directory = "frames"
	output_path = "result.png"
    
	#combine_images(input_directory, output_path)

	image_paths = [os.path.join(input_directory, filename) for filename in os.listdir(input_directory) if filename.endswith(".png")]
	image_paths.sort()

	for ip in image_paths:
		im2 = replace_black_bg_with_white(ip)
		im2 = remove_black_bg(im2)
		cv2.imwrite(f"nova/{output_path}", cv2.bitwise_not(im2))
