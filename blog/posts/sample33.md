title: Factory Functions
date: 2088-08-09
subtitle: This a subtitle


# Factory Functions

In languages such as Java, C# and some other languages there is only one way appropriate way to instantiate an object.
However because javascript is the odd child this creates a few reasons to be weary about letting javascript play with `Classes`.
Let me explain.

```js
  class Armor {
    constructor(){
    this.superheroName = 'Iron Man'
    this.power = 'plasma'
  }

  activate(){
    console.log(` A wild ${this.superHeroName} has appeared! ` );
  }

  fires(){
    console.log(
    `${this.superheroName} shoots ${this.power} at enemy` );
    }
  }

  const tony_stark = new Armor()

  tony_stark.activate() // Outputs: "˛ A wild Iron Man has appeared! "
  tony_stark.fires() // Outputs: "Iron Man shoots plasma at enemy"
```

Here is a particulary mundane class. The class ( which in this case a super ability ) has a constructor and two methods 'activate' and 'fires'.
We this code creates an instance of the Armor ablilty declared as the variable 'tony_stark.

*Note: Given the underlying nature of javascripts prototypical object creation this is not an instance in the strict sense  howeever, further definition is a seperate topic which should be researched if it is not understood already. For the sake of the blog we will assume this to be an instance in the traditional sense of the word.*

After declaring the new instance of Armor we call both available methods consecutively. The methods then output the template strings in an expected way.

This would generally be fine however there are problems with when we take into account javascript's design. For example take this:

``` javascript
$(div.newMovie).dblclick(tony_stark.fires())
```

In the case of this snippet the code breaks. The code breaks because by the nature of 'Class' style instantiation the instance variables declared in the constructor ( `this.superheroName` & `this.power` ) lose context. Given the matter by which the `this` keyword works when call in an event handler as shown above the `this` will refer to the window element rather than the Armour. Simply put if the code is written that way when we double-click we the template string will call refer to `window.superheroName` and `window.power` instead of `Armour.superheroName` and `Armour.power`

Such an issue can be fixed in the the normal weird javascript way by re-writing the code like so...

```javascript
$(div.newMovie).dblclick(tony_stark.fires.bind(this))
```

Or like so ...

```javascript
//Using ES6 arrow functions
$(div.newMovie).dblclick( () => tony_stark.fires )
```

## Barely passing

This is a adequate, and quite common solutions... but it feels janky like really janky. Often time ( especially when written many times in a session ) `.bind(this)` feels like one of those 'fixes but not fixes'. Like passing an exam with a 65%. Or like fixing a constantly shutting window by putting a book in it to wedge it open. Even more so when the reference you trying to circumvent isn't even a DOM Element.

But there is a hope.

As said before in many langauges class are the only means to instantiate an object or dictate ( or express inheritance ). However, in javascript there is often another way.

## Factory Functions

Let's try this again but written as a factory function.

``` javascript
//Using ES6
const armour  = () => {
    const superheroName = "Iron Man" ;
    const power = "plasma"
    return {

    activate: () => {
      console.log(
          `A wild ${superHeroName} has appeared!` );
    },
    fires: () => {
      console.log(
          `${superheroName} shoots ${power} at enemy` );
    }

    }
}
```


So here is the rundown. We have a function. Inside that function two local variables are declared `superheroName` and `power`. The function terminates with an `Object` being the return value. We create and instance of our Armoured superhero as such...

``` javascript
const tony_stark = new armour()
```

and we call the 'methods' as such...

``` javascript
tony_stark.activate(); // Outputs: "A wild Iron Man has appeared"
tony_stark.fires(); // Outputs: "Iron Man shoots plasma at enemy"
```

When a we instatiate objects in this way we resolve a lot of issues. Firstly,  our issue of variables losing context is rememdied because the `Object` being returned is making reference to variables called within the scope of the function. So...

``` javascript
$(div.newMovie).dblclick(tony_stark.fires())
// Works without needing to bind anymore 🎉🎉
```

Secondly, creating instances using factory function is by far is much easier to reason about and makes changes far easier to implement down the road. Furthermore, the code is written in such a way that we are leveraging the javascript's unique behaviors in a way that make keeps the flow code simple and , in my opinions, easier to read.

### Caveats

**Factory Functions** have a mild draw back. ``Classes`` (those things you should still stop using now ) are indeed faster. comparitively they the instance as described above will talk around 0.0002s to run where a factory function is double that at 0.0004s. However unless you are literally attempting to write 1000 `Classes` per frame ( which in itself is a problem ) factory function are still the bette Option.

## Conclusion
- Factory Function are a different way to create object in javascript and are better then ``Classes`` (they just are).
- They are less convaluted then `Classes`
- They utilize closure to prevent the need to use `this' or lose context when calling 'methods' elsewhere in your code.


Stay Frosty!!!


### P.S.

It was mentioned that how the function works works may be a tad bit confusing. Especially to those newer to javascript. So lets consider this.

```javascript
//First we create a factory function
const armour  = () => {
    const superheroName = "Iron Man" ;
    const power = "plasma"
    return {

    activate: () => {
      console.log(
          `A wild ${superHeroName} has appeared!` );
    },
    fires: () => {
      console.log(
          `${superheroName} shoots ${power} at enemy` );
    }

    }
}

//Next we declare a instance of that function.

const james_rhodes = new armour()

/*
Because we a returning an object in the function. What we are esstianly creating via a function is this
*/

const james_rhodes = {
    activate: () => {
      console.log(
          `A wild ${this.superHeroName} has appeared!` );
    },
    fires: () => {
    console.log(
    `${this.superheroName} shoots ${this.power} at enemy` );
}

/*Note: That the function returns the values as refered to by the placeholders.
So that "${this.superheroName}" and  "${this.power}" are replaced with
"War Machine" and "plasma" respectivley. */

}

/* Everytime we create an instance of the `armour`
we are essentially creating an object like the one above.
Only with a diffrent variable name.
And like the object we can functions via dot notation as such */

james_rhodes.fire()
```
