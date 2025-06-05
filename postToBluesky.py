from atproto import Client

# Define a function to post an image to Bluesky
# This function takes a username, password, and image file path as input
# It logs into Bluesky, formats a post with hashtags, and sends the image as part of the post

def post_image_to_bsky(username, password, file_path):
    """
    Posts a local image to Bluesky with a hardcoded caption and clickable hashtags.

    Args:
        username (str): Your Bluesky handle (e.g., "you.bsky.social")
        password (str): Your Bluesky app password
        file_path (str): Path to the local image file
    """
    # Create a client instance from the atproto package
    client = Client()

    # Login to the Bluesky account using the provided credentials
    client.login(username, password)

    # Open the image file in binary mode and read its contents
    with open(file_path, 'rb') as f:
        img_data = f.read()  # Read binary data from the file

    # Set the main caption text for the post
    caption = "This is a Bluesky post with an image! \n\n"

    # Define a list of hashtags to be appended to the post
    hashtags = ['#These', '#Are', '#Hashtags']

    # Prepare the rich_text dictionary which includes the full text and hashtag metadata
    rich_text = {"text": caption, "facets": []}  # facets list stores clickable tag positions

    # Keep track of the current character position in the post text
    position = len(caption)

    # Iterate through each hashtag to append it to the caption and mark its position
    for tag in hashtags:
        start = position  # Starting byte of the tag in the string
        end = start + len(tag)  # Ending byte of the tag

        # Add the tag and a space to the rich text content
        rich_text["text"] += tag + " "

        # Move the position pointer forward for the next hashtag
        position += len(tag) + 1

        # Add metadata for the hashtag so it becomes a clickable tag in the post
        rich_text["facets"].append({
            "index": {"byteStart": start, "byteEnd": end},  # Define where the tag starts and ends
            "features": [
                {"$type": "app.bsky.richtext.facet#tag", "tag": f"{tag[1:]}"}  # Remove '#' when defining tag name
            ]
        })

    # Send the composed post including the image and formatted text
    client.send_image(
        text=rich_text["text"],           # Full caption including hashtags
        facets=rich_text["facets"],       # Metadata making hashtags clickable
        image=img_data,                    # Raw image data to attach
        image_alt='Example Bluesky Post'   # Alt text for accessibility
    )

# Execute the function if the script is run as the main program
if __name__ == "__main__":
    post_image_to_bsky(
        username = "YOUR_HANDLE.bsky.social",    # Replace with your Bluesky handle
        password = "YOUR_PASSWORD",     # Replace with your app password (keep secure!)
        file_path= 'img.png'                  # Path to the image file to be posted
    )

    print("Post Succesful!")
