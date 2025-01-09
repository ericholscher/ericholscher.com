```{post} Jan 08, 2025
:category: link-blog
```

# Exploring CSS Variables

We're looking at ways to make Read the Docs more customizable while using [web components](https://developer.mozilla.org/en-US/docs/Web/Web_Components) to build our UI.
One of the ways we're exploring is using [CSS variables](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties) to allow users to customize the look and feel of their documentation.

This is something we're already starting to support,
but it was good to see [Shoelace](https://shoelace.style/getting-started/customizing#design-tokens) doing similar things.

This would look something like:

```css
    :root {
        /* Reduce Read the Docs' flyout font a little bit */
        --readthedocs-flyout-font-size: 0.7rem;
        /* Reduce Read the Docs' notification font a little bit */
        --readthedocs-notification-font-size: 0.8rem;
        /* This customization is not yet perfect because we can't change the `line-height` yet. */
        /* See https://github.com/readthedocs/addons/issues/197 */
        --readthedocs-search-font-size: 0.7rem;
    }
```

I'm curious if folks have any other good examples of these being used in the wild,
or feedback on how we're thinking about using them.