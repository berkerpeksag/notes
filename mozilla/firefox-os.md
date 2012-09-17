# There is something magical about Firefox OS

Over the past year and a half I've been spending more and more of my time working with Mozilla's latest project, Firefox OS. During that time I've fallen in love with the project and what it stands for, in ways that I've never experienced with a technology platform before.

![](http://farm9.staticflickr.com/8456/7980043535_c6a39de9c8_o.jpg)

Let me be perfectly clear; Firefox OS is the start of something huge. It's a revolution in waiting. A breath of fresh air. A culmination of bleeding-edge technology. It's magical and it's going to change everything.

## What is Firefox OS?

For those of you wondering what on earth I'm on about, let me bring you up to speed.

> Firefox OS is a new mobile operating system developed by Mozilla's Boot to Gecko (B2G) project. It uses a Linux kernel and boots into a Gecko-based runtime engine, which lets users run applications developed entirely using HTML, JavaScript, and other open Web application APIs.
>
> &ndash; [Mozilla Developer Network](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS)

In short, Firefox OS is about taking the technologies behind the Web, like JavaScript, and using them to produce an entire mobile operating system. Just let that sink in for a moment — it's a mobile OS powered by JavaScript!

To do this, a slightly-customised version of Gecko (the engine behind Firefox) has been created that introduces the new [JavaScript APIs necessary to create a phone-like experience](https://wiki.mozilla.org/WebAPI#APIs). This includes things like WebTelephony to make phone calls, WebSMS to send text messages, and the Vibration API to, well, vibrate things.

[video:http://youtu.be/5MzuGWFIfio]

But Firefox OS is much more than the latest Web technologies being used in crazy ways, as awesome as that is, it's also a combination of many other projects at Mozilla into a single vision — the Web as a platform. Some of these projects include our [Open Web Apps initiative](https://developer.mozilla.org/en-US/docs/Apps) and [Persona](https://login.persona.org/about), our solution to identity and logins on the Web (formally known as BrowserID). It's absolutely fascinating to see so many different projects at Mozilla coalesce into a single, coherent vision.

I'll leave the description there as this entry isn't about explaining the project in fine detail, though more information can be found on the [Firefox OS pages on MDN](https://developer.mozilla.org/en-US/docs/Mozilla/Firefox_OS). I definitely recommend checking them out.

## Why Firefox OS?

So you might be thinking, "This sounds great, but why use JavaScript to build a phone?" And you'd be right, that's a really important question to ask. The good news is that there are plenty of reasons why this is a good idea, besides making Web developers weak at the knees.

The two major reasons are that Firefox OS fills a gap in the mobile market, and that it provides an alternative to the current proprietary and restrictive mobile landscape.

### Closing a gap in the mobile market

It's no surprise to anyone that smartphones are often ridiculously expensive, even in areas of the world that are perceived to have high levels of income. But if you thought they were expensive in countries that have the disposable income to afford them, consider for a moment that [a 16GB iPhone 4S costs the equivalent of £615](http://store.apple.com/br/browse/home/shop_iphone/family/iphone/iphone4s) in a developing market like Brazil — that's over £100 more expensive than the same phone in the UK!

Now, those inflated prices in Brazil are mainly down to high levels of import tax. Apple are apparently working to avoid that in the future by building local production lines in the country. Regardless, it points out a key issue in that expensive, high-end devices aren't always an option in all areas of the world. Let alone the fact that in some societies [you might not want to publicly brandish a phone the price of a small car](http://en.wikipedia.org/wiki/Crime_in_Brazil).

So what do you do if you want a smartphone experience without shelling out a stupid amount of money? You could turn to the cheap Android devices but they tend to run poorly.

Fortunately, this is where Firefox OS comes in…

> The goal of Firefox OS isn't to compete with high-end devices, but to offer entry- to mid-level smartphones at feature phone prices.
>
> &ndash; [Bonnie Cha](http://allthingsd.com/20120906/mozilla-makes-a-mobile-web-browser-feel-like-a-smartphone)

Firefox OS fits this gap in the market perfectly. It offers a smartphone experience on cheap, low-end hardware that is comparable to an Android experience on mid-range hardware. That is not a joke.

For example, I am currently testing JavaScript games on a Firefox OS device that costs £50 (arguably, a very low-end device). You may expect them to run pretty poorly but they not only run much faster than the same games running in an Android browser (Firefox or Chrome) on the same device, they run as fast, if not faster than the same game running in an Android browser on a much better device that costs 4 or 5 times as much.

Why the huge performance improvements over browsers in Android on identical devices? It's because of the lack of stuff going on between Gecko and the hardware, meaning things like JavaScript can run at full pelt. So much for JavaScript being slow!

This JavaScript performance on such cheap hardware is one of the reasons why I'm convinced that Firefox OS is the beginning of something huge.

*I should point out that Mozilla isn't necessarily launching with a £50 device, it's just one that we're currently using for development and testing.*

### Providing an alternative, open platform

The second reason for 'Why Firefox OS?' is that it's an attempt to not only provide an open alternative mobile platform, but to stand up to and try and influence the big proprietary mobile players to change things.

> Mozilla's mission since its outset in 1998, first as a software project and later as a foundation and company, has been to provide open technology that challenges a dominant corporate product.

> &ndash; [Steve Lohr](http://bits.blogs.nytimes.com/2012/02/23/why-mozilla-is-entering-the-smartphone-war/)

Mozilla is attempting to replicate its success with Firefox, in which it stormed the browser market and showed users that there is an alternative, one that lets them be in control of how they use the Web.

> This time, it's the mobile Web that's threatened, not by Microsoft but by Apple and Google, the leading smartphone platforms. With their native apps, locked-down platforms, proprietary software stores, and capricious developer rules, Apple and Google are making Web technology less relevant.
>
> &ndash; [Thomas Claburn](http://www.informationweek.com/development/mobility/mozillas-firefox-os-seeks-innovation-wit/240007065)

On mobile, one of the main areas that needs improving is application portability…

> For all the excitement around mobile apps, they seem a step backward in one respect: they tie users to a particular operating system and devices that support it. The Web, by contrast, evolved so that content is experienced much the same way on any hardware.
> Mozilla, maker of the Firefox Web browser, is determined to make the same thing true for smartphones.
>
> &ndash; [Don Clark](http://blogs.wsj.com/digits/2012/09/06/backers-tout-firefox-os-as-open-mobile-option/)

What Firefox OS aims to do here is to use the native everywhere-ness of the Web to provide a platform that allows applications to be enjoyed on a mobile device, a desktop computer, a tablet, or anywhere else that has access to a browser. Wouldn't you want to be able to pick up your Angry Birds game on the desktop where where you left it on your phone? I certainly would!

### A hackable dream for developers

One final, extra reason why Firefox OS is needed is that we don't really have a comparable hackable mobile platform at the moment (you can sort of customise Android but it's not easy).

Because Firefox OS is constructed using HTML, JavaScript and CSS it means you only need basic Web development skills to reach in and completely change the device experience. You could literally change one line of CSS and completely change the way the icons on the homescreen look, or re-write some core JavaScript files that handle phone-calls.

It's truly a platform for developers and I'm most excited about seeing where they take it beyond Mozilla's vision.

## Perfect timing

Something that I've been fully aware of during my year-and-a-half at Mozilla is how fortunate I am to be here for the beginning of the Firefox OS project. If I remember right, it was announced (as Boot to Gecko) internally during my first few weeks on the job.

Things were exciting back then but boy have they become even more exciting over time. Firefox OS is literally the number 1 thing that I'm working on at the moment and I honestly love it, I actually feel privileged to be a part of it.

I've wondered many times if this is how it felt to work at Mozilla during the initial launch of Firefox; the excitement, passion, nervousness, and inability to explain quite how amazing it all is and why people should care.

To be honest, I don't think many people will truly understand what's happening with Firefox OS and why it really matters until long after it has launched. A little like Firefox, I suppose.

For now, I'm happy to be at Mozilla at a very interesting point in its life.

## Blown minds

The people who do get it right now are the developers that have been hands-on with the demo devices that occasionally come with Mozillians to events. There's not much I enjoy more than watching their expressions as they go through the various stages of emotion while playing with the devices…

1. It starts with mild confusion — a sort of 'Why have you just given me an Android device?' look
2. Following confusion is sudden realisation that this isn't Android, it's built using JavaScript
3. After a short while the excitement starts in a sort of "Holy shit!" mind-blowing moment
4. A while longer and they're deep in concentration, exploring every corner of the device and asking lots of questions
5. The last stage is slight reluctance as I ask for the device back and a final "That wasn't half bad, I'm impressed!" as they hand it over

You'd think I made that up to make things sound all rosy and amazing, but I honestly get those exact reactions from so many people that I show the devices to. It's actually quite funny.

What I've come to realise is that the more I see others play on a Firefox OS device the more I'm convinced that it's a real game-changer. It just seems blows minds left right and centre, with barely any explanation needed from me.

## Plenty of challenges

It wouldn't be fair to talk about the greatness of Firefox OS and the things I'm working on without covering some of the challenges that we need to solve.

On one side there are the more general issues, like how to manage an apps ecosystem that's open and unrestrictive, or possible device fragmentation like there is with Android. Those issues are important but are ultimately uninteresting to me.

However, what I'm most interested in is the challenge we have with HTML5 games on mobile devices — both the perceived and very real performance issues that developers often complain about. This is by no means an issue specific to Firefox OS (Android and iOS are just as bad) but right now I'm purely focussed on Firefox OS and how we can improve things there.

As it stands, the majority of pre-existing HTML5 games for mobile either run really poorly (0—20FPS), or sort of alright (20—30FPS). Most of the time these games don't run at a stable frame-rate either, which makes the experience not very enjoyable.

What's interesting is that a lot of the issues don't necessarily seem to be with the device or with JavaScript. There are a few intense games, like [Biolab Disaster](http://playbiolab.com/), that perform stunningly on even the £50 low-end device that I'm testing on — we're talking between 40 and 60FPS.

It's definitely clear to me that, although the devices and platform are sometimes to blame (not as often as some would like to make out), there is a lot we can learn from the games that do perform well on the low-end devices to see what techniques they're using and how best to educate other developers looking to target HTML5 on mobile devices.

I truly believe that quite intense HTML5 games can run well on mobile devices, even low-end ones. Why am I so confident about that? Because people are already making those games today. There are 2 things that I trust most in my life… my eyes.

We'll get there.

## Beyond the mobile phone

What excites me most about Firefox OS has nothing to do with the mobile device that we're launching next year but is instead about what the future holds. I touched on this earlier when talking about Firefox OS being a hackable dream, how others could take it and extend it beyond Mozilla's vision.

[video:http://youtu.be/rk1oTO6cYH0]

The great news is that this is already happening today. We already have a [port of Firefox OS for the Raspberry Pi](http://www.youtube.com/watch?v=rk1oTO6cYH0), as well as [one for the Pandaboard](https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/Pandaboard). They aren't perfect, but what's awesome (I've tried so hard to avoid that word) is that this has all happened before Firefox OS has even reached it's first release.

You also have the ability to [run Firefox OS via a desktop client](https://developer.mozilla.org/en-US/docs/Mozilla/Boot_to_Gecko/Using_the_B2G_desktop_client) on Mac, Windows, and Linux. While not giving you the same hardware access as you get on a device, the desktop client allows you to benefit from the other features of the OS (like apps running in separate processes) and is fairly easy to set up.

I can just imagine a day in the not-to-distant future where the Gamepad API has landed in Gecko and can be accessed via the Firefox OS desktop client. What's so cool about that? Well it's not a giant stretch of the imagination to see that desktop client being run on a device connected to a TV, with the OS customised to use gamepad input instead of mouse and touch (it's all JavaScript, remember).

What you'd have there is the beginnings of a HTML5 games console, and it's actually something I'm keen to explore in my 'free' time outside of Mozilla.

My point here is that we're coming to a point in time where devices can now be powered by the same technologies that we would normally use to build websites. What could we do with a world full of devices powered by those technologies, that can all access and communicate with the same APIs?

I'm desperate to see what that world looks like!