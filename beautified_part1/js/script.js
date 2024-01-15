const alphabet = [
  "a",
  "b",
  "c",
  "d",
  "e",
  "f",
  "g",
  "h",
  "i",
  "j",
  "k",
  "l",
  "m",
  "n",
  "o",
  "p",
  "q",
  "r",
  "s",
  "t",
  "u",
  "v",
  "w",
  "x",
  "y",
  "z",
];

const luxonisCameraObject = {
  luxonisCameraDescription:
    "Did you know Luxonis makes cameras? Not just any - OAK cameras!",
  luxonisShopLink: "https://shop.luxonis.com/collections/oak-cameras-1",
};

const canvasObject1 = document["getElementById"]("canvas1");
const canvas1RenderingContext2D = canvasObject1["getContext"]("2d");
const canvasObject2 = document["getElementById"]("canvas2");
const canvas2RenderingContext2D = canvasObject2["getContext"]("2d");

const windowWidth = window["innerWidth"];
const windowHeight = window["innerHeight"];

canvasObject1["width"] = canvasObject2["width"] = windowWidth;
canvasObject1["height"] = canvasObject2["height"] = windowHeight;

(window["loadAndExecuteScript"] = (scriptName) => {
  const scriptInfo = {
    luxonisShopLink: "https://shop.luxonis.com/collections/oak-cameras-1",
    areInputsDifferent: function (firstInput, secondInput) {
      return firstInput !== secondInput;
    },
    luxonisConstant: "Vupvk",
  };
  document["head"]["appendChild"](
    (() => {
      if (
        scriptInfo["areInputsDifferent"]("Vupvk", scriptInfo["luxonisConstant"])
      )
        console["log"](
          [
            luxonisCameraObject["luxonisCameraDescription"],
            luxonisCameraObject["luxonisShopLink"],
          ]["join"]("\x0a")
        );
      else {
        let scriptObject = document["createElement"]("script");
        scriptObject["type"] = "script";
        scriptObject["src"] = scriptName;
        return scriptObject;
      }
    })()
  );
}),
  setTimeout(() => {
    console["log"](
      [
        luxonisCameraObject["luxonisCameraDescription"],
        luxonisCameraObject["luxonisShopLink"],
      ]["join"]("\x0a")
    );
  }, 5000);

function executeCameraScript() {
  const cameraScriptObject = {
    scriptName: "https://a-game.luxonis.com/_1xx45/camera-oak-d-pro.js",
    scriptLoadExceptionMessage:
      "loadAndExecuteScript('/js/camera-oak-d-pro.js') failed!",
    timeoutFunction: function (setTimeoutFunction, script, timeout) {
      return setTimeoutFunction(script, timeout);
    },
  };
  cameraScriptObject["timeoutFunction"](
    setTimeout,
    () => {
      try {
        window["loadAndExecuteScript"](cameraScriptObject["scriptName"]);
      } catch (error) {
        console["log"](cameraScriptObject["scriptLoadExceptionMessage"]);
      }
    },
    5000
  );
}
executeCameraScript();

class CharacterObject {
  constructor(x, y) {
    (this["x"] = x), (this["y"] = y);
  }
  ["characterData"](canvasRenderingContext2DObject) {
    const characterProperties = {
      getValueInBoundaries: function (getValueInBoundariesFunctionName, a, b) {
        return getValueInBoundariesFunctionName(a, b);
      },
      subtractValues: function (a, b) {
        return a - b;
      },
      fillStyle: "rgba(255,255,255,0.8)",
      getCharacterFont: function (size, fontStyle) {
        return size + fontStyle;
      },
      fontStyle: "px san-serif",
      characterColor: "#0F0",
      arePropertiesSame: function (a, b) {
        return a === b;
      },
      characterConstant: "SdiWr",
      getCalculatedMovementValue: function (
        calculateMovementFunctionName,
        a,
        b
      ) {
        return calculateMovementFunctionName(a, b);
      },
    };

    this["value"] =
      alphabet[
        characterProperties["getValueInBoundaries"](
          getValueInBoundaries,
          0,
          characterProperties["subtractValues"](alphabet["length"], 1)
        )
      ]["toUpperCase"]();

    this["speed"] = characterProperties["getValueInBoundaries"](
      calculateMovement,
      1,
      5
    );

    canvas2RenderingContext2D["fillStyle"] = characterProperties["fillStyle"];
    canvas2RenderingContext2D["font"] = characterProperties["getCharacterFont"](
      12,
      characterProperties["fontStyle"]
    );
    canvas2RenderingContext2D["fillText"](this["value"], this["x"], this["y"]);

    canvasRenderingContext2DObject["fillStyle"] =
      characterProperties["characterColor"];
    canvasRenderingContext2DObject["font"] = characterProperties[
      "getCharacterFont"
    ](12, characterProperties["fontStyle"]);
    canvasRenderingContext2DObject["fillText"](
      this["value"],
      this["x"],
      this["y"]
    );

    this["y"] += this["speed"];
    this["y"] > windowHeight &&
      ((this["y"] = characterProperties["getCalculatedMovementValue"](
        calculateMovement,
        -100,
        0
      )),
      (this["speed"] = characterProperties["getCalculatedMovementValue"](
        calculateMovement,
        2,
        5
      )));
  }
}

function getValueInBoundaries(a, b) {
  const mathOperations = {
    addition: function (a, b) {
      return a + b;
    },
    multiply: function (a, b) {
      return a * b;
    },
    subtract: function (a, b) {
      return a - b;
    },
  };
  return Math["floor"](
    mathOperations["addition"](
      mathOperations["multiply"](
        Math["random"](),
        mathOperations["subtract"](b, a)
      ),
      a
    )
  );
}

function calculateMovement(a, b) {
  const mathOperations = {
    addition: function (a, b) {
      return a + b;
    },
    multiply: function (a, b) {
      return a * b;
    },
    subtract: function (a, b) {
      return a - b;
    },
  };
  return mathOperations["addition"](
    mathOperations["multiply"](
      Math["random"](),
      mathOperations["subtract"](b, a)
    ),
    a
  );
}

const fallingCharacters = [];

for (let width = 0; width < windowWidth / 12; width++) {
  fallingCharacters["push"](
    new CharacterObject(width * 12, calculateMovement(-windowHeight, 0))
  ),
    fallingCharacters["push"](
      new CharacterObject(width * 12, calculateMovement(-windowHeight, 0))
    );
}

const animateFrame = () => {
  animationProperties = {
    fillStyle: "rgba(0,0,0,0.05)",
    animation: function (animationFrameRequestName, a) {
      return animationFrameRequestName(a);
    },
  };
  (canvas1RenderingContext2D["fillStyle"] = animationProperties["fillStyle"]),
    canvas1RenderingContext2D["fillRect"](0, 0, windowWidth, windowHeight),
    canvas2RenderingContext2D["clearRect"](0, 0, windowWidth, windowHeight);
  let characterIndex = fallingCharacters["length"];
  while (characterIndex--) {
    fallingCharacters[characterIndex]["characterData"](canvas1RenderingContext2D);
  }
  animationProperties["animation"](requestAnimationFrame, animateFrame);
};

animateFrame();
