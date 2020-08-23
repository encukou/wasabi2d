Post-processing effects
=======================

Wasabi2d provides a small number of pre-defined full-screen post processing
effects. These are defined at the layer level, and affect items in that layer
only.

.. method:: Layer.set_effect(name, **kwargs)

    Set the effect for the layer to the given name. Return an object that
    can be used to set the parameters of the effect.

.. method:: Layer.clear_effect()

    Remove the active effect.


Available effects
-----------------

The effects are described here as separate calls:


.. method:: Layer.set_effect('bloom', radius: float=10, gamma: float = 1.0, intensity: float = 0.5)

    Create a light bloom effect, where very bright pixels glow, making them
    look exceptionally bright. The radius controls how far the effect reaches.

    .. versionadded:: 1.3.0

        Added the `gamma` and `intensity` parameters.

    .. image:: _static/effects/bloom.png
        :alt: Example of the light bloom effect


.. method:: Layer.set_effect('trails', fade: float=0.9, alpha: float = 1.0)

    Apply a "motion blur" effect. Fade is the fraction of the full brightness
    that is visible after 1 second.

    Alpha is the overall intensity of the effect.

    .. image:: _static/effects/trails.png
        :alt: Example of the trails effect


.. method:: Layer.set_effect('punch', factor: float=1.0)

    Apply a pinch/punch effect.

    A factor greater than 1.0 creates a "punch" effect; objects near the center
    of the camera are enlarged and objects at the edge are shrunk.

    A factor less than 1.0 creates a "pinch" effect; objects near the center of
    the camera are shrunk and objects at the edge are enlarged.

    .. image:: _static/effects/punch.png
        :alt: Example of the punch effect

    .. image:: _static/effects/pinch.png
        :alt: Example of the pinch effect


.. method:: Layer.set_effect('blur', radius: float=10.0)

    Apply a full screen gaussian blur.

    ``radius`` is the maximum radius of the blur.

    The effect runs on the GPU but larger radiuses are more costly to compute.
    The cost of the effect is *O(radius)*.

    .. image:: _static/effects/blur.png
        :alt: Example of the blur effect


.. method:: Layer.set_effect('pixellate', pxsize: int=10, antialias: float=1.0)

    Pixellate the contents of the layer. ``pxsize`` is the output pixel size.

    By default, this effect computes the average value within each pixel, ie.
    antialiases as it downsamples.

    For a more retro look, disable the antialiasing by passing ``antialias=0``.
    Values between 0 and 1 will give a weaker antialiasing effect; values
    greater than 1 give an even more blurred look.

    The effect runs on the GPU but with antialiasing, larger pxsizes are more
    costly to compute. The cost of the effect is *O(pxsize * antialias)*.

    .. versionadded:: 1.3.0

    .. image:: _static/effects/pixellate.png
        :alt: Example of the pixellate effect, with antialiasing on and off


.. method:: Layer.set_effect('dropshadow', radius: float=10.0, opacity: float=1.0, offset: Tuple[float, float]=(1.0, 1.0))

    Apply a drop-shadow effect: draw an offset, blurred copy layer underneath
    the normal layer contents.

    :param radius: The maximum radius of the blur.
    :param opacity: The opacity of the shadow; 1.0 is black, lower values make
                    the shadow partially transparent.
    :param offset: The offset of the shadow in screen pixels. ``(1, 1)``
                   offsets the shadow downwards and to the right. Note that
                   this is a screen-space effect and these coordinates are
                   always in screen space.

    .. versionadded:: 1.1.0

    .. image:: _static/effects/dropshadow.png
        :alt: Example of the drop shadow effect


.. method:: Layer.set_effect('greyscale', amount: float=1.0)

    Convert colours to greyscale or partially desaturate them.

    :param amount: The fraction of the colour to remove; 0.0 means keep full
                   colour, while 1.0 is fully black and white.

    .. versionadded:: 1.3.0

    .. image:: _static/effects/greyscale.png
        :alt: Examples of the greyscale effect


.. method:: Layer.set_effect('sepia', amount: float=1.0)

    Convert colours to sepia.

    Sepia is similar to greyscale effect in that it desaturates, but the sepia
    spectrum is slightly warmer, like an old photograph.

    :param amount: The fraction of the colour to remove; 0.0 means keep full
                   colour, while 1.0 is fully sepia.

    .. versionadded:: 1.3.0

    .. image:: _static/effects/sepia.png
        :alt: Examples of the sepia effect


.. method:: Layer.set_effect('posterize', levels: int=2, gamma: float=0.7)

    Map colours to a reduced palette.

    ``levels`` specifies the number of levels in each channel to reduce to
    (plus 0); the total number of colours will be ``levels ** 3``. For example,
    with ``levels=2`` the colours will be black, red, green, blue, yellow,
    cyan, magenta and white.

    ``gamma`` deserves particular attention. ``gamma`` is applied when
    calculating how the levels fall in the ``[0, 1]`` interval. When
    ``gamma=1``, levels will fall at regular intervals. Gamma less than 1
    dedicates more bands to dark colours, and few bands to light colours;
    gamma greater than 1 dedicates more bands to light colours, and more to
    dark colours. The overall brightness of the image does not change so much,
    but these can give very different effects, perhaps suiting different
    graphic styles.

    :param levels: The number of levels in each channel.
    :param gamma: A power expressing the spacing of the levels.

    .. versionadded:: 1.3.0

    .. image:: _static/effects/posterize.png
        :alt: Examples of the posterize effect


.. tip:: Effects Examples

    Each effect has an interactive example in the ``examples/effects/``
    directory in the `wasabi2d repository`__.

    Try cloning this repository and running the examples in order to better
    understand the effects.

.. __: https://github.com/lordmauve/wasabi2d/tree/master/examples/effects


.. _chain:


The Chain
---------

.. versionadded:: 1.3.0

So far we've seen effects that apply to just one layer. This is a pretty quick
way to get impressive results.

However, this system is limited to acting on one layer at a time, and one
effect at a time.

To better customise rendering, we need to take a different approach; this is
called **the chain**.

.. attribute:: scene.chain

    A list of ChainNodes that define how the scene is rendered. The list is
    rendered in order, so later items render on top of earlier items.

    The default value for a new scene is::

        scene.chain = [wasabi2d.chain.LayerRange()]

This gives the default strategy for rendering the scene: to simply render
all layers from back (lowest id) to front (highest id). This is implemented
by the LayerRange node:

.. autoclass:: wasabi2d.chain.LayerRange

There's a similar class that makes it easier to nominate specific layers:

.. autoclass:: wasabi2d.chain.Layers


Each of these classes subclasses `ChainNode`, which means that they can be
wrapped in an effect. Effects can also be wrapped in effects.


.. autoclass:: wasabi2d.chain.ChainNode
    :members:


.. tip::

    Layers are, fundamentally, for organising primitives. The chain is for
    configuring how the scene renders, even as layers come and go.

    Layer effects straddle this: they apply to layers, but affect how the
    scene renders. Think of this as a convenience - a way of getting started
    with effects, before putting them onto the chain.


Chain-Only Effects
------------------

In addition to applying the above effects, some effects can only be applied
via the chain.

.. class:: wasabi2d.chain.Mask

    Paint one node, ``paint`` masked by another node, the ``mask``. By default,
    the paint layer is drawn where the mask is opaque; other functions are
    available.

    .. attribute:: paint

        A chain node that will be painted, subject to the mask.

    .. attribute:: mask

        A chain node that forms the mask. Only the alpha channel from this node
        is used.

    .. attribute:: function

        One of ``inside``, ``outside``, or ``luminance``. Defines what aspect
        of the mask layer is used to calculate the alpha channel:

        * ``inside`` - draw the paint layer where the mask is opaque.
        * ``outside`` - draw the paint layer where the mask is transparent.
        * ``luminance`` - draw the paint layer with more opacity where the mask
          is bright (white), and more transparency where it is dark.

    For example::

        scene.chain = [
            w2d.chain.Mask(
                w2d.chain.Layers([1]),
                w2d.chain.LayerRange(stop=0),
            )
        ]

    This code uses layer 1 as a mask for all layers 0 and below. Now if we put
    an opaque circle on layer 1, and a photo on layer 0::

        scene.layers[0].add_sprite('positano', pos=center)
        scene.layers[1].add_circle(radius=200, pos=center)

    It renders like this:

    .. image:: _static/effects/mask.png
        :alt: Examples of rendering an image inside a mask


.. class:: wasabi2d.chain.DisplacementMap

    Paint one node, ``paint`` offset by the image given by the ``displacement``
    node.

    The colour channels of the displacement layer give the offset to displace
    by; the alpha channel selects how much of the paint layer to show (much
    like a mask).

    By default, the red channel of the displacement layer controls x offset,
    while the green channel controls y offset. This can be overridden by
    setting the ``x_channel`` and ``y_channel`` attributes.

    The value of the offset is calculated as distance from the 0.5 mid-point.
    A mid grey - ``#7f7f7f`` - represents no offset.

    .. attribute:: paint

        A chain node that will be painted, subject to the mask.

    .. attribute:: displacement

        A chain node that gives the displacement (And alpha value).

    .. attribute:: scale

        A float; the distance that is offset at maximum.

    .. attribute:: x_channel

        Either ``'r'``, ``'g'``, or ``'b'``: the channel that gives the offset
        in the *x* direction.

    .. attribute:: y_channel

        Either ``'r'``, ``'g'``, or ``'b'``: the channel that gives the offset
        in the *y* direction.

    For example::

        scene.chain = [
            w2d.chain.LayerRange(stop=0),
            w2d.chain.DisplacementMap(
                displacement=w2d.chain.Layers([1]),
                paint=w2d.chain.LayerRange(stop=0),
                scale=400
            )
        ]

    This code renders layers below 0 normally, as well as drawing layer 1 with
    a "refraction" of those layers.

    A displacement map that gives a lens-like effect might be this one:

    .. image:: _static/effects/lens.png
        :alt: Example lens image

    It renders like this:

    .. image:: _static/effects/displacement.png
        :alt: Examples of rendering a displacement effect


.. class:: wasabi2d.chain.Fill

    Fill the scene with a colour.

    Overwrites everything, even if the colour given has partial transparency.

    This is primarily useful as input to an effect like Mask.

    .. attribute:: color

        The colour that will be used to fill the buffer.

.. class:: wasabi2d.chain.Light

    .. versionadded:: 1.5.0

    Use one input as a light map to light the other input.

    .. attribute:: light

        A chain node that contains the light map. Primitives in these layers
        will be drawn with additive blending.

    .. attribute:: diffuse

        A chain node that is the base image to be lit.

    .. attribute:: ambient

        A colour which gives the ambient light level, ie. the amount of the
        diffuse input which is visible even if there are no lights.

        This defaults to black, ie. pitch black.

    As a worked example, we might set up a chain effect that defines a single
    light layer (layer 99), that lights all layers up to and including layer 1:

    .. code-block:: python

        scene.chain = [
            chain.Light(
                light=99,
                diffuse=chain.LayerRange(stop=1),
                ambient='#333333'
            ),
        ]

    The lights can be sprites. We need some special sprites for this. Here are
    some examples. These work as is (black means no light), or
    you can use images with an alpha channel.

    .. figure:: _static/effects/point-light.png

        A sprite that is suitable as a point light.

    .. figure:: _static/effects/bat_light.png

        This sprite represents the light pool cast by a bat in the Pong example.

    The Pong example, which can be found in ``examples/pong`` in
    `the repository <https://github.com/lordmauve/wasabi2d/>`__, illustrates
    this lighting effect, with shaped lights on the bat and a point light that
    tracks the ball.

    .. image:: _static/effects/pong.png
