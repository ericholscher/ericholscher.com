```{post} Jan 13, 2025
:category: link-blog
```

# [AI in tech writing roundup](https://technicalwriting.dev/ml/reviews/2024.html#ml-reviews-2024)

The topic of AI is all the rage in the tech writing industry of late.
This [round up from Kayce
Basques](https://technicalwriting.dev/ml/reviews/2024.html#ml-reviews-2024)
is a great overview of all the various use cases, and the status of them
in the industry:

> #### Basic content generation
>
> > *ChatGPT can generate paragraphs or sections based on given topics
> > or outlines, providing a starting point for technical writers. This
> > can speed up the content creation process and help maintain
> > consistency in writing.*
>
> There's a lot of this happening. Tom Johnson has been using a prompt
> engineering approach to [automate release notes
> authoring](https://idratherbewriting.com/ai/automating-linking.html).
> I have also automated some of my changelog process with moderate
> success. Manny Silva is [extensively automating first draft
> work](https://aws.amazon.com/blogs/machine-learning/how-skyflow-creates-technical-content-in-days-using-amazon-bedrock/).
> I can recall many more anecdotes like this.
>
> \[...\]
>
> #### Grammar and spell-checking
>
> > *ChatGPT can identify and correct grammatical errors, spelling
> > mistakes, and other language inconsistencies, leading to
> > higher-quality content.*
>
> I have heard of technical writers using LLMs for one-off editing
> tasks. E.g. they were given the first draft of a new doc written by a
> software engineer (or product manager, or whatever) and were told that
> the doc must be published in a couple hours. The first draft had a lot
> of errors and typos. To meet the ridiculous deadline the writers fed
> the first draft through an LLM to quickly fix the major issues.
>
> --- [Kayce
> Basques](https://technicalwriting.dev/ml/reviews/2024.html#ml-reviews-2024)

I had a pretty interesting experience with GitHub Copilot where I was
able to [catch 3-4 cases of misplaced
words](https://github.com/writethedocs/www/pull/2291/commits/450a16ce1066bf269e0257a8c68daf1f9ca69fdd)
in a blog post recently. This is something that is really hard to catch
when you're reading your own content, and it was a great use.

#### How the sausage was made

I used the following prompt, which was actually partially generated from
ChatGPT:

![](/_static/img/substack/another-good-tech-writing-roundup_image_1.png)

Then I updated it with a couple additional things to watch out for:

> Please review the following blog post for:
>
> 1\. Correct Markdown syntax, ensuring proper formatting for headings,
> links, lists, code blocks, and images.
>
> 2\. Grammar and spelling, suggesting any necessary corrections.
>
> 3\. Suggestions to improve clarity or readability where needed.
>
> 4\. Consistent use of capitalization.
>
> 5\. Consistent use of grammar rules like oxford commas.

I got this idea from [a Reddit post with some recommended prompts for
reviewing
content](https://www.reddit.com/r/ChatGPTPromptGenius/comments/16q68iq/op_prompts_to_edit_refine_your_writing/).

I think that getting an automated "third party" review of content is a
pretty powerful use of generative tools.
