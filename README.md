# Image Genie
#### Video Demo:  https://www.youtube.com/watch?v=CAJIIqB7uEw
#### Description:  This work was inspired by Rick Strahl's Weblog - Integrating OpenAI Image Generation into a .NET Application.

Images serve as a universal mode of communication, seamlessly integrated into various mediums such as blog posts, webpages, and applications as glyphs.

Image generation offers a pathway to translate imaginative concepts into visual representations. Achieving effective image generation hinges on the use of well-constructed prompts. This necessitates familiarity with prompting best practices, attainable through research, experimentation, and guidance from conversational AI systems, such as ChatGPT.

To alleviate the challenge of mastering prompt crafting, an intuitive human inquiry interface is embedded within the Image Genie, facilitating effective image generation without the need for extensive prompt crafting expertise.

The implementation adheres to the principles of DALL-E 3, prioritizing concise image generation prompts limited to 4,000 characters in length.

Note: You will need to perform the following for this application to run successfully...

1. Replace the OpenAI API key with a valid value, in ImageGeneration.OpenApi.KEY in the imagegeneration.py file.
2. Run the imagegenerationdb.py program to seed the TinyDb database.
3. Run the project.py program.

## Project Composition

### project.py
This module contains the mainline code and has been significantly influenced by the CS50 Final Project requirements.

### test_project.py
This module showcases the ability to write Python (pytest) test scripts and has been significantly influenced by the CS50 Final Project requirements.

### imagegeneration.py
This module houses the ImageGeneration class, which is responsible for handling the details of Image Generation. DALL-E 3 is utilized for Image Generation,
though it does not explicitly support negative prompts (instructing DALL-E not to include certain elements). The design emphasizes providing DALL-E 3 with
a succinct prompt, focusing on the desired outcome within a length of less than 4,000 characters. The user interface is implemented using the Python Inquirer
library (https://github.com/magmax/python-inquirer) due to its simplistic design and ability to run within the GitHub Codespace development environment.

### imagegenerationdb.py
This module houses the ImageGenerationDb class, which follows a data persistence "bridge" design pattern. It provides an abstraction of data persistence from
its implementation, allowing the data access interface and data persistence to be defined and extended independently from each other. TinyDB, a lightweight
Python database library, is utilized, and this is the only class in the project that has knowledge or interaction with its implementation.

### openai_image_dto.py
This module contains the OpenAiImageDto class, representing the OpenAI Image response data transfer object (DTO). It serves as a "bridge" between the actual
OpenAI Image response and what is provided as the image to its consumers.

### httpclient.py
This module contains the HttpClient class, which provides HTTP client string constants in a reusable fashion.

https://weblog.west-wind.com/posts/2023/Dec/21/Integrating-OpenAI-image-generation-into-your-NET-Application
https://keithtorrence.substack.com/p/the-master-guide-to-prompting-dall
