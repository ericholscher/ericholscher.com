```{post} Jan 18, 2025
:category: link-blog
```

# Alternative company structures

I ran into this [Ask HN
post](https://news.ycombinator.com/item?id=42748394) from [Dave
Snider](https://www.davesnider.com/), which asks about alternative
company structures:

> Long story short, I\'m building a new product and will likely launch
> it as a yearly SaaS with a permissive license. I\'m later in my career
> and am mostly building it for fun, but I think it has potential to be
> a good, small business that I\'d have fun fiddling with for a long
> time.
>
> I went through and set up the usual LLC, but was curious about how I
> could set it up to be a member or worker-owned company. Has anyone
> done anything like that from the beginning? Should I just worry about
> this later?

This is something that I've been wondering about ever since going to
DazzleCon 2017 from [Zebras Unite](https://zebrasunite.coop/). That
group had a lot of people building organizations with alternative
structures.

## Some interesting comments

On the Ask HN post, there were a couple comments that I thought were
good ways to think about this.

### Non-profit owning the for-profit

> The key thing was to keep the SaaS-y bit as boring as possible, which
> meant a corporation. This is in Europe but the equivalent would be
> Delaware C corp.
>
> Shares in the corporation were then given to the wrapping organization
> (in my case the foundation, but this could be more-or-less any legal
> structure that can have assets). Downside is two sets of accounts,
> upsides are that M&A gets a ton easier later on, and taking on
> employees is simple and not colored by the legal quirks of the parent
> organization. The potential complexity of SaaS accounting (revenue
> recognition, R&D credits, etc) is also kept inside a simple, normal
> corporation which every CPA is super-familiar with, so you\'re not
> consulting niche experts every time something new comes up.

This is a model I've seen a few places where there's an operating
entity, and a non-profit of some sort that holds the assets and uses the
profits. Novo Nordisk has a [split legal
structure](https://en.wikipedia.org/wiki/Novo_Holdings_A/S), as well as
[Mozilla](https://en.wikipedia.org/wiki/Mozilla_Foundation).

It isn't exactly what Dave was asking about, but it's a common structure
that seems reasonably widely used.

### Profit sharing

> I established a limited liability company (LLC) for a business venture
> initiated with friends. My objective was to ensure that all
> contributors received a fair share of the equity while maintaining a
> simplified structure for tax purposes. Additionally, I wanted to
> ensure that equity shares did not confer voting rights, functioning
> instead as profit-sharing interests. Legal counsel assisted in
> structuring the entity as a single-member LLC, where I am the sole
> owner, with profit-sharing units allocated to other contributors. This
> arrangement entitles contributors to a defined percentage of the
> company's profits and proceeds from events such as a sale of the
> company.

This is a path we've taken with [Read the
Docs](https://about.readthedocs.com/), where we specify a profit sharing
agreement with everyone on the team who works there. This doesn't
currently transfer to a longer term ownership of profit, but I think
there's a lot of merit to this as opposed to equity. I'm not an
accountant, but I believe it avoids a lot of the tax issues that come
with equity grants, but again haven't done permanent grants that might
trigger a tax liability at this point in our organization.

I don't have any great links for other folks that have done this, but I
know it's a somewhat common structure in venture debt and
[non-traditional investment funding
agreements](https://github.com/indievc/terms/blob/master/term_sheet_v3.md)
to take a percentage of profit or revenue after a certain time period.

## My worries

I think there is a beauty to the idea of sharing ownership with the
membership of a service. Dave mentioned this in the comments:

> Open source just gives away the code, without setting up resources for
> the people who work on it. If I charge for the service, which is owned
> by the members, I could presumably pay upkeep (hosting, dedicated
> workers\...etc).

This is a beautiful vision, but I think it would be hard implement in
practice. I'm trying to imagine how a pitch like this might work. Do you
offer the customer/members some kind of profit sharing? A discount on
future services?

Given that customers often want to avoid lock-in on any purchasing
decision, it seems hard to build a service that has a larger up front
psychological and legal commitment. I love the idea of getting bonus
points in life for building structures with collaborative ownership, but
realistically most people and businesses only want a simple "buy a
service that I can cancel" relationship.

That said, I\'d love to see someone try it! I think it could work well
in a niche environment, or something like a Kickstarter where people
feel they helped bring something into being.
