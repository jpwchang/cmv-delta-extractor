import sys

def extract_deltas(submission, return_comment_dict=False):
    # we will return a list of comment IDs that earned deltas
    delta_comments = []
    # first, we build a dictionary for fast lookup of comments by ID
    comment_dict = {}
    for comment in submission["comments"]:
        comment_dict[comment["name"]] = comment
    # now, we scan through the comments looking for the generic post by
    # DeltaBot marking the giving of a delta
    for i, comment in enumerate(submission["comments"]):
        sys.stdout.write("\r[DeltaExtractor] searching comment %d of %d" % (i+1, len(comment_dict)))
        # there seem to be some dummy comments in the dataset lacking any text.
        # we should just ignore these.
        if "body" not in comment:
            continue
        # when a delta is awarded, DeltaBot will comment saying "Confirmed: 1
        # delta awarded to <author>"
        if comment["author"] == "DeltaBot" and "delta awarded" in comment["body"]:
            # now that we have found a delta, we must locate the comment that it
            # was awarded to. This is not nearly as straightforward as just finding
            # the grandparent comment, because in a long chain of comments the
            # author's main argument might actually be buried somewhere farther
            # up. As a heuristic, we treat the *longest* comment by the delta'd
            # author as the one that received the delta.
            parent = comment_dict[comment["parent_id"]]
            grandparent = comment_dict[parent["parent_id"]]
            author = grandparent["author"]
            # start with the assumption that the grandparent comment is the
            # delta'd comment...
            longest_comment_id = grandparent["name"]
            longest_comment_len = len(grandparent["body"])
            # ...then work our way backward up the comment chain looking for
            # other comments by the same author
            cur_comment = grandparent
            while cur_comment["parent_id"] in comment_dict:
                cur_comment = comment_dict[cur_comment["parent_id"]]
                if cur_comment["author"] == author:
                    if len(cur_comment["body"]) > longest_comment_len:
                        longest_comment_id = cur_comment["name"]
                        longest_comment_len = len(cur_comment["body"])
            delta_comments.append(longest_comment_id)
    sys.stdout.write("\n")
    print("Found %d deltas is this submission" % len(delta_comments))
    if return_comment_dict:
        return (delta_comments, comment_dict)
    else:
        return delta_comments
