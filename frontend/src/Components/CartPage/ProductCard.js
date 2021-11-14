import React, { useState, useEffect } from "react";
import axios from "axios";
import { connect } from "react-redux";

// Libraries
import classNames from "classnames";

// @material-ui components
import { makeStyles } from "@material-ui/core/styles";
import Paper from "@material-ui/core/Paper";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";
import ButtonBase from "@material-ui/core/ButtonBase";
import Checkbox from "@material-ui/core/Checkbox";
import ButtonGroup from "@material-ui/core/ButtonGroup";
import AddCircleIcon from "@material-ui/icons/AddCircle";
import RemoveCircleIcon from "@material-ui/icons/RemoveCircle";
import Divider from "@material-ui/core/Divider";
import { ThemeProvider } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import Snackbar from "@material-ui/core/Snackbar";
import MuiAlert from "@material-ui/lab/Alert";

// local components
import styles from "../../styles/js/CartPage/CartPageStyle.js";
import product1 from "../../assets/HomePage/product1.png";
import theme from "../../consts/theme";
import { fetchCart } from "../../store/actions/cart";
import {
  removeFromCartURL,
  addToCartURL,
  removeAllFromCartURL,
  rapidMobile,
  userDetailsURL,
  rapidSMS,
  rapidEmail,
} from "../../consts/constants";

const useStyles = makeStyles(styles);

function ProductCard(props) {
  const Alert = React.forwardRef(function Alert(props, ref) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
  });
  const { token, fetchCart, authenticated } = props;
  const [username, setUserName] = useState("");
  const [open, setOpen] = React.useState(false);
  const [sopen, setSopen] = React.useState(false);
  useEffect(() => {
    if (authenticated) {
      axios
        .get(userDetailsURL, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((res) => {
          setUserName(res.data.userid);
        })
        .catch((err) => {
          console.log(err.response);
        });
    }
  }, [authenticated, token]);

  const handleClick = () => {
    setOpen(true);
  };
  const handleSClick = () => {
    setSopen(true);
  };

  const add = (slug) => {
    axios
      .post(
        addToCartURL,
        { pslug: slug },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      .then((res) => {
        if (res.status === 200) {
          console.log("added succesfully");
          fetchCart();
        }
      })
      .catch((err) => {
        console.log("not added ");
        console.log(err.response);
      });
  };
  const sendOrder = (products) => {
    var p = JSON.parse(JSON.stringify(products));
    delete p["token"];
    p["contact"] = username;
    axios
      .post(
        rapidMobile,
        {
          phone: "+918960734951",
          text: JSON.stringify(p),
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: "617bf1b7245383001100f7d6",
          },
        }
      )
      .then((res) => {
        handleClick();
      });
    axios
      .post(rapidEmail, {
        owner_id: "67417601",
        token: "uUDVKVwyNfZubR2SjgTHBZey",
        smtp_user_name: "smtp23203123",
        message: {
          html: "Example HTML content",
          text: "Example text content",
          subject: "example subject",
          from_email: "noreply@rapidemail.rmlconnect.net",
          from_name: "Example Name",
          to: [
            {
              email: "dpsman13016@gmail.com",
              name: "hljkhjl",
              type: "to",
            },
          ],
          headers: {
            "Reply-To": "noreply@rapidemail.rmlconnect.net",
            "X-Unique-Id": "id ",
          },
        },
      })
      .then((res) => {
        handleSClick();
      });
  };
  const subtract = (slug) => {
    axios
      .post(
        removeFromCartURL,
        {
          pslug: slug,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      .then((res) => {
        if (res.status === 200) {
          fetchCart();
        }
      })
      .catch((err) => {
        console.log("Error");
      });
  };
  const removeAll = (slug) => {
    axios
      .post(
        removeAllFromCartURL,
        {
          pslug: slug,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      .then((res) => {
        if (res.status === 200) {
          fetchCart();
        }
      })
      .catch((err) => {
        console.log("Error");
      });
  };
  const classes = useStyles();

  return (
    <ThemeProvider theme={theme}>
      <div className={classes.root}>
        <Paper className={classes.paper}>
          <Grid container spacing={2}>
            <Grid item>
              <Checkbox defaultChecked color="primary" />
              <ButtonBase className={classes.image}>
                {/* Todo image  */}
                <img className={classes.img} alt="complex" src={product1} />
              </ButtonBase>
            </Grid>
            <Grid item xs={12} sm container>
              <Grid item xs container direction="column" spacing={2}>
                <Grid item xs>
                  <Typography
                    gutterBottom
                    variant="subtitle1"
                    style={{ fontWeight: "bold" }}
                  >
                    {props.name}
                  </Typography>
                  <Typography gutterBottom variant="body2">
                    {/* Todo seller details */}
                    Sold By: {props.sellerName}
                  </Typography>
                  <Typography
                    variant="body2"
                    gutterBottom
                    style={{ color: "green" }}
                  >
                    In stock
                  </Typography>
                  <div style={{ display: "flex" }}>
                    <Typography
                      variant="body2"
                      gutterBottom
                      style={{ fontWeight: "bold" }}
                    >
                      &#8377;{props.price}
                    </Typography>
                    <Typography
                      className={classNames(classes.cartText, classes.text)}
                      variant="body2"
                      color="textSecondary"
                    >
                      &#8377;{props.mrp}
                    </Typography>
                    <Typography
                      className={classes.cartText}
                      variant="body2"
                      gutterBottom
                      style={{ color: "green" }}
                    >
                      You save &#8377;50.00
                    </Typography>
                  </div>
                </Grid>
                <Grid item>
                  <Typography
                    variant="body2"
                    style={{ cursor: "pointer", color: "#7D808E" }}
                  >
                    <span
                      onClick={() => {
                        removeAll(props.slug);
                      }}
                    >
                      Remove
                    </span>{" "}
                    | Save For Later | See More Like This
                  </Typography>
                </Grid>
              </Grid>
              <Grid item>
                <Typography variant="subtitle1"> </Typography>
                <Typography variant="subtitle1"></Typography>
              </Grid>
            </Grid>
            <Grid item>
              <ButtonGroup>
                <RemoveCircleIcon
                  onClick={() => subtract(props.slug)}
                  style={{ color: "#37b3f9", cursor: "pointer" }}
                ></RemoveCircleIcon>
                <div
                  style={{
                    minWidth: "15px",
                    marginLeft: "1px",
                    textAlign: "center",
                  }}
                >
                  {props.quantity}
                </div>
                <AddCircleIcon
                  onClick={() => add(props.slug)}
                  style={{ color: "#37b3f9", cursor: "pointer" }}
                ></AddCircleIcon>
              </ButtonGroup>
            </Grid>
          </Grid>
          <Divider className={classes.divider} orientation="horizontal" />
          <div>
            <Typography
              style={{
                display: "flex",
                justifyContent: "flex-end",
                fontWeight: "bold",
              }}
              variant="body2"
            >
              Subtotal : &#8377; {props.subtotal}
              <Button
                variant="contained"
                color="primary"
                style={{ marginLeft: "3vw" }}
                onClick={() => sendOrder(props)}
              >
                Send order to shopkeeper
              </Button>
            </Typography>
          </div>
        </Paper>
      </div>
      <Snackbar open={open} autoHideDuration={6000}>
        <Alert severity="success" sx={{ width: "100%" }}>
          Order sent to shopkeeper
        </Alert>
      </Snackbar>
      <Snackbar open={sopen} autoHideDuration={6000} key={"bottom" + "left"}>
        <Alert severity="success" sx={{ width: "100%" }}>
          Order receipt sent to your email address
        </Alert>
      </Snackbar>
    </ThemeProvider>
  );
}

const mapStateToProps = (state) => {
  return {
    token: state.auth.token,
    authenticated: state.auth.token !== null,
  };
};
const mapDispatchToProps = (dispatch) => {
  return {
    fetchCart: () => dispatch(fetchCart()),
  };
};
export default connect(mapStateToProps, mapDispatchToProps)(ProductCard);
